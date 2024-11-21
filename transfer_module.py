from dcim.models import Module, Device, ModuleBay
from extras.scripts import Script, ObjectVar
from django.core.exceptions import ValidationError
from django.db import transaction

class TransferModule(Script):
    class Meta:
        name = "Přesun modulu"
        description = "Přesune modul do jiného zařízení a zkontroluje, zda cílové zařízení již modul neobsahuje."

    selected_module = ObjectVar(
        model=Module,
        label="Modul k přesunu",
        description="Vyberte modul, který chcete přesunout."
    )
    target_device = ObjectVar(
        model=Device,
        label="Cílové zařízení",
        description="Vyberte zařízení, do kterého bude modul přesunut."
    )
    target_module_bay = ObjectVar(
        model=ModuleBay,
        label="Cílový module bay (volitelné)",
        required=True,  # Povinný, protože modul musí být přiřazen k module bay
        query_params={
            'device_id': '$target_device',
        },
        description="Vyberte module bay na cílovém zařízení."
    )

    def run(self, data, commit):
        selected_module = data['selected_module']
        target_device = data['target_device']
        target_module_bay = data['target_module_bay']

        self.log_debug(f"Vybraný modul: {selected_module}")
        self.log_debug(f"Cílové zařízení: {target_device}")
        self.log_debug(f"Cílový module bay: {target_module_bay}")

        # Kontrola, zda cílové zařízení již obsahuje modul stejného typu
        existing_module = Module.objects.filter(device=target_device, module_type=selected_module.module_type).first()
        if existing_module:
            self.log_warning(f"Cílové zařízení '{target_device}' již obsahuje modul '{existing_module}'. Přesun byl zrušen.")
            return

        try:
            with transaction.atomic():
                # 1. Odpojení modulu od původního module bay
                original_module_bay = ModuleBay.objects.filter(module=selected_module).first()
                if original_module_bay:
                    self.log_debug(f"Odpojuji modul z původního module bay: {original_module_bay}")
                    original_module_bay.module = None
                    if commit:
                        original_module_bay.save()

                # 2. Aktualizace zařízení a přiřazení k cílovému module bay
                self.log_debug(f"Nastavuji zařízení modulu '{selected_module}' na '{target_device}'.")
                selected_module.device = target_device
                selected_module.module_bay = target_module_bay
                if commit:
                    selected_module.save()

                # Logování úspěšné akce
                self.log_success(f"Modul '{selected_module}' byl úspěšně přesunut do zařízení '{target_device}' a přiřazen k module bay '{target_module_bay}'.")

        except ValidationError as e:
            self.log_failure(f"Přesun modulu se nezdařil: {e}")
        except Exception as e:
            self.log_failure(f"Nastala neočekávaná chyba: {e}")
