class AppConstants {
  //api endpoints
  static const String notesEndpoint = '/notes';
  static const String flashcardsEndpoint = '/flashcards';
  static const String authEndpoint = '/auth';
  static const String aiEndpoint = '/ai';
  static const String chatEndpoint = '/chat';
  static const String analyticsEndpoint = '/analytics';

  //pagination
  static const int defaultPageSized = 10;
  static const int maxPageSized = 50;

  //file upload
  static const int maxImageSize = 10 * 1024 * 1024; //10mb
  static const List<String> allowedImageTypes = ['jpg', 'jpeg', 'png', 'webp'];
  //cache keys
  static const Duration apiTimeout = Duration(seconds: 30);
  static const Duration cacheExpiry = Duration(hours: 24);
  //limits
  static const int maxTitleLength = 100;
  static const int maxContentLength = 10000;
  static const int maxTagsLength = 200;
}
