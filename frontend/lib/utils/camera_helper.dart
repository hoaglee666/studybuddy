import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:permission_handler/permission_handler.dart';

class CameraHelper {
  static final ImagePicker _picker = ImagePicker();
  //check camera permis
  static Future<bool> checkCameraPermission() async {
    final status = await Permission.camera.status;
    if (status.isGranted) {
      return true;
    }
    final result = await Permission.camera.request();
    return result.isGranted;
  }

  //check gallery permis
  static Future<bool> checkGalleryPermission() async {
    final status = await Permission.photos.status;
    if (status.isGranted) {
      return true;
    }
    final result = await Permission.photos.request();
    return result.isGranted;
  }

  //take photo from camera
  static Future<XFile?> takePhoto() async {
    final hasPermission = await checkCameraPermission();
    if (!hasPermission) {
      return null;
    }
    try {
      return await _picker.pickImage(
        source: ImageSource.camera,
        maxWidth: 1920,
        maxHeight: 1080,
        imageQuality: 85,
      );
    } catch (e) {
      debugPrint('Error taking photo: $e');
      return null;
    }
  }

  //gallery
  static Future<XFile?> pickImage() async {
    final hasPermission = await checkGalleryPermission();
    if (!hasPermission) {
      return null;
    }
    try {
      return await _picker.pickImage(
        source: ImageSource.gallery,
        maxWidth: 1920,
        maxHeight: 1080,
        imageQuality: 85,
      );
    } catch (e) {
      debugPrint('Error picking images: $e');
      return null;
    }
  }

  //selection dialog
  static Future<XFile?> showImageSourceDialog(BuildContext context) async {
    return await showModalBottomSheet<XFile?>(
      context: context,
      builder: (context) => SafeArea(
        child: Wrap(
          children: [
            ListTile(
              leading: const Icon(Icons.camera_alt),
              title: const Text('Take photo'),
              onTap: () async {
                Navigator.pop(context);
                final image = await takePhoto();
                if (context.mounted) {
                  Navigator.pop(context, image);
                }
              },
            ),
            ListTile(
              leading: const Icon(Icons.photo_library),
              title: const Text('Choose from gallery'),
              onTap: () async {
                Navigator.pop(context);
                final image = await pickImage();
                if (context.mounted) {
                  Navigator.pop(context, image);
                }
              },
            ),
            ListTile(
              leading: const Icon(Icons.cancel),
              title: const Text('Cancel'),
              onTap: () async {
                Navigator.pop(context);
              },
            ),
          ],
        ),
      ),
    );
  }
}
