# CBZ Editor

A simple GUI application for editing CBZ comic archives with image management capabilities.

![Screenshot](https://cloud.tacnet.co.uk/s/9jSEayTHmntdYwC/preview)

## Features

- Edit CBZ files (add/remove/reorder images)
- Batch create CBZ files from folder structures
- Integrated image editing with external software
- Dark theme interface
- Keyboard shortcuts for efficient workflow
- Customizable thumbnail viewing

## Requirements

- Python 3.6+
- Pillow library

## Installation

1. Clone/download repository
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run `CBZ Editor.pyw`

1. Open a CBZ file or a folder of images.
2. Edit images (opens in default image editor).
3. Use keyboard shortcuts for quick actions.
4. Save changes with automatic naming.

### Essential Hotkeys:

- **Ctrl+O**: Open CBZ
- **Ctrl+S**: Save and next
- **Ctrl+W**: Close and next
- **←/→**: Navigate between CBZs
- **V**: Overwrite and next
- **Q**: Toggle delete behavior

### Image Editing Tip

For best results, set your preferred image editor (e.g., Photoshop, GIMP) as the default program for opening JPG/PNG files. The editor will automatically open images in your default software.

## License

This project is licensed under the MIT License. See the [License.txt](/License.txt) file for details.

See `CHANGELOG.md` for version history and updates.
