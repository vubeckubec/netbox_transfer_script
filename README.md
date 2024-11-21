# Transfer Module Script for NetBox

This script, `TransferModule`, is designed for NetBox to facilitate the transfer of a module from one device to another while ensuring that the target device does not already contain a module of the same type. It also allows assigning the module to a specific module bay on the target device.

## Features
- **Validation**: Ensures the target device does not already contain a module of the same type before proceeding.
- **Atomic Transaction**: Uses a database transaction to ensure data integrity during the transfer process.
- **Detailed Logging**: Logs debug, success, and failure messages to assist in monitoring and troubleshooting.
- **Customizable**: Allows users to specify the module, target device, and target module bay.

## Requirements
- **NetBox version**: Ensure compatibility with your NetBox version.
- **Models used**:
  - `dcim.models.Module`
  - `dcim.models.Device`
  - `dcim.models.ModuleBay`

## Usage

### Parameters
1. **`selected_module`**: The module to be transferred.
   - Type: `Module`
   - Description: Select the module you want to transfer.
2. **`target_device`**: The device to which the module will be transferred.
   - Type: `Device`
   - Description: Select the target device.
3. **`target_module_bay`**: The module bay on the target device where the module will be assigned.
   - Type: `ModuleBay`
   - Description: Select the target module bay on the target device.
   - Required: Yes

### Execution
Make sure that you have rqworker running!
1. Navigate to the **Scripts** section in the NetBox UI.
2. Select the `Transfer Module` script.
3. Fill out the required fields:
   - **Module to Transfer**: Select the module you wish to move.
   - **Target Device**: Select the device to which the module will be transferred.
   - **Target Module Bay**: Specify the module bay for the target device.
4. Run the script.

### Script Logic
1. **Validation**:
   - Checks if the target device already has a module of the same type as the selected module.
   - If found, the operation is aborted with a warning message.
2. **Detachment**:
   - Detaches the selected module from its current module bay (if applicable).
3. **Transfer**:
   - Assigns the module to the target device and module bay.
4. **Save Changes**:
   - Saves the changes if the operation is successful.

## Error Handling
- **ValidationError**: Captures and logs any validation issues during the transfer.
- **General Exception**: Handles and logs unexpected errors.

## Example Output
- **Success**:
Modul 'Module1' byl úspěšně přesunut do zařízení 'Device2' a přiřazen k module bay 'ModuleBay1'.

- **Failure**:
Přesun modulu se nezdařil: Modul již existuje na cílovém zařízení.

## Notes
- Ensure that all required fields are filled out before executing the script.
- Test the script in a development environment before using it in production.
- Use this script with proper permissions to avoid unintended changes.

## License
This script is provided "as is" without any guarantees. Use at your own risk.
