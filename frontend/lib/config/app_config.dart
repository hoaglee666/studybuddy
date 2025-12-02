class AppConfig {
  //api config
  static const String baseUrl = 'http://10.0.2.2:8000';
  static const String apiUrl = '$baseUrl/api';
  static const String wsUrl = 'ws://10.0.2.2:8000/ws';
  //timeouts
  static const Duration connectionTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(seconds: 30);
  //storage keys
  static const String accessTokenKey = 'access_token';
  static const String refreshTokenKey = 'refresh_token';
  static const String userDataKey = 'user_data';
  //pagina
  static const int defaultPageSize = 10;
  // file upload
  static const int maxFileSize = 10 * 1024 * 1024; //10mb
  //oauth
  static const String googleClientId = '';
}
