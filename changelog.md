#### 

# CBZ Editor Change Log


## v1.7.0 (Help Panel & Structure Flattening Update)

Release Summary: Added help panel, structure flattening, and new hotkeys for improved usability.

#### Features:

- Introduced a help panel (accessible via the "?" button) displaying all hotkeys and their functions.
- Added "v" keybinding to trigger overwrite-and-next functionality.
- Added "q" keybinding to toggle "Swap sort on Delete" behavior.
- Implemented automatic folder structure flattening to handle CBZ files with nested images/subdirectories.
- Added a "Fix Folder Structure" button when nested images are detected.
- Enhanced overwrite feedback with button flashing for visual confirmation.

#### Bug Fixes:

- Fixed improper handling of duplicate filenames during structure flattening.
- Resolved UI glitches when nested image detection triggered the fix-structure button.
- Addressed XML file cleanup errors during flattening operations.

#### Improvements:

- Streamlined file monitoring to ignore intentionally deleted files.
- Improved error logging for structure-flattening processes.
- Optimized help panel positioning and styling to match the dark theme.
- Enhanced hotkey documentation and accessibility via the help panel.

---

## v1.6.0 (Overwrite Save & UI Refinements)

Release Summary: Added overwrite save functionality and improved UI elements.

#### Features:

- Introduced "Overwrite" button to save changes without renaming CBZ files.
- Improved UI layout for better accessibility and clarity.
- Added automatic season and chapter recognition in filenames.

#### Bug Fixes:

- Fixed an issue where swapping sort order on delete was inconsistent.
- Addressed UI inconsistencies with checkbox styles.

#### Improvements:

- Optimized file save logic to handle overwrites smoothly.
- Enhanced error handling and file monitoring for better stability.

---

## v1.5.0 (File Monitoring & Deletion Fixes)

Release Summary: Improved file monitoring stability and addressed deletion inconsistencies.

#### Features:

- Enhanced file monitoring to prevent accidental reloading of deleted images.
- Added additional error handling when deleting files to prevent crashes.

#### Bug Fixes:

- Fixed a bug where deleted files were being re-monitored and causing UI issues.
- Resolved an issue where the "Save" button styling would not reset correctly after a deletion.

#### Improvements:

- Optimized background monitoring to reduce CPU usage.
- Improved deletion handling to ensure files are fully removed before updating the UI.

---

## v1.4.1 (Enhanced Sorting & UI Improvements)

Release Summary: Improved sorting functionality and UI feedback.

#### Features:

- Added a label update when toggling "Swap sort on Delete" for better user feedback.
- Improved sorting logic to maintain consistency when deleting images.

#### Bug Fixes:

- Fixed an issue where the UI did not update properly after toggling sorting settings.
- Addressed a bug that caused duplicate sort toggles when deleting images.

#### Improvements:

- Adjusted sorting toggles to work more predictably when "Swap sort on Delete" is enabled.
- Improved UI responsiveness when deleting and updating images.

---

## v1.4.0 (Swap Sort on Delete & Performance Enhancements)

Release Summary: Introduced a new setting for toggling sort behaviour on deletion and improved stability.

#### Features:

- Added "Swap sort on Delete" checkbox to toggle automatic sorting behavior when deleting images.
- Enhanced file monitoring to better track changes and avoid unnecessary refreshes.

#### Bug Fixes:

- Fixed a bug where file monitoring would attempt to reload deleted images.
- Addressed an issue where deleted images could still appear in saved CBZ files.

#### Improvements:

- Optimized deletion handling to prevent UI flickering.
- Improved error handling and logging for better debugging.

---

## v1.3.1 (Thumbnail Update & Image Refresh Fix)

Release Summary: Improved thumbnail refresh, image updates, and bug fixes.

#### Features:

- Added real-time thumbnail update for modified images without needing a full refresh.
- Implemented automatic image update detection to reload only the affected thumbnails.
- Fixed an issue where deleted images were not being removed from the UI properly.

#### Bug Fixes:

- Resolved a bug where sorting order was not properly maintained after refreshing thumbnails.
- Fixed a UI issue where images did not update correctly after being edited externally.

#### Improvements:

- Optimized image monitoring for better performance.
- Improved handling of image deletion and UI updates to prevent inconsistencies.

---

## v1.3.0 (Image Monitoring & Auto-Save Update)

Release Summary: Added real-time image monitoring and improved file saving logic.

#### Features:

- Implemented real-time monitoring for opened images to detect changes and update thumbnails automatically.
- Added automatic deletion of old CBZ files after renaming to avoid duplication.

#### Bug Fixes:

- Fixed an issue where deleted images were still included in saved CBZ files.

#### Improvements:

- Enhanced file save process to preserve modifications and maintain folder structure.
- Improved error handling when monitoring image changes.

---

## v1.2.1 (Hotkey Management Update)

Release Summary: Improved user input management and hotkey handling.

#### Features:

- Implemented hotkey activation tracking to prevent accidental actions while typing.
- Disabled hotkeys when the series name input box is focused and re-enabled on focus out.

#### Bug Fixes:

- None reported.

#### Improvements:

- Moved the series name input field above the save button for better UI layout.
- Improved responsiveness of hotkey interactions for a smoother experience.

---

## v1.2.0 (Series Naming)

Release Summary: Added series name input, partial image refresh, and improved file renaming.

#### Features:

- Added input field for entering series name.
- Implemented partial refresh to load only the top 4 images for quicker display.
- Enhanced batch processing for CBZ creation.

#### Bug Fixes:

- Fixed minor UI inconsistencies when switching sorting order.

#### Improvements:

- Improved file renaming to follow "Series Name - cXXX.cbz" format.
- Optimized refresh process for smoother navigation.

---

## v1.0.0 (Initial Release)

Release Summary: First version of the CBZ Editor codebase.

Features:

- Implemented core CBZ file management functionalities.
- Added dark theme UI.
- Enabled opening, editing, and saving CBZ files.
- Included batch CBZ creation from ZIP files.
- Thumbnail previews for images within CBZ files.
- Implemented keyboard shortcuts for navigation and saving.

#### Bug Fixes:

- None (initial release).

#### Improvements:

- None (initial release).

---

## v1.1.1 (Thumbnail Refresh Update)

Release Summary: Added functionality to refresh thumbnails and improved sorting status updates.

#### Features:

- Introduced "r" keybinding to refresh thumbnails.
- Sorting order label now updates dynamically when loading a new CBZ file.

#### Bug Fixes:

- None reported.

#### Improvements:

- Improved handling of UI updates for sorting order.
- Optimized image loading performance for better responsiveness.

---

## v1.1.0 (Sorting Update)

Release Summary: Added sorting functionality and improved user interaction.

#### Features:

- Introduced image sorting functionality (ascending/descending order toggle).
- Added "s" keybinding to switch sorting order.
- Display sorting order status in the UI.

#### Bug Fixes:

- None reported.

#### Improvements:

- Reset sorting order when loading a new CBZ file.
- Enhanced UI elements for better clarity.
