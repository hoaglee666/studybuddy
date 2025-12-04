import 'package:google_sign_in/google_sign_in.dart';
import 'package:studybuddy/models/user.dart';
import 'package:studybuddy/services/api_service.dart';
import 'package:studybuddy/services/storage_service.dart';

class AuthService {
  final ApiService _apiService = ApiService();
  final StorageService _storageService = StorageService();
  final GoogleSignIn _googleSignIn = GoogleSignIn(scopes: ['email', 'profile']);

  //register
  Future<User> register(String email, String name, String password) async {
    try {
      final response = await _apiService.post(
        '/auth/register',
        data: {'email': email, 'name': name, 'password': password},
      );
      if (response.statusCode == 200) {
        //save token
        await _storageService.saveTokens(
          response.data['access_token'],
          response.data['refresh_token'],
        );
        return await getCurrentUser();
      } else {
        throw Exception('Registration failed');
      }
    } catch (e) {
      throw Exception(_apiService.handleError(e));
    }
  }

  Future<User> login(String email, String password) async {
    try {
      final response = await _apiService.post(
        '/auth/login',
        data: {'username': email, 'password': password},
      );
      if (response.statusCode == 200) {
        await _storageService.saveTokens(
          response.data['access_token'],
          response.data['refresh_token'],
        );
        return await getCurrentUser();
      } else {
        throw Exception('Login failed');
      }
    } catch (e) {
      throw Exception(_apiService.handleError(e));
    }
  }

  Future<User> signInWithGoogle() async {
    try {
      final GoogleSignInAccount? googleUser = await _googleSignIn.signIn();
      if (googleUser == null) {
        throw Exception('Google sing in cancelled');
      }
      final GoogleSignInAuthentication googleAuth =
          await googleUser.authentication;
      throw Exception('Google sign in not imple');
    } catch (e) {
      throw Exception('Google sign in failed: ${e.toString()}');
    }
  }

  Future<User> getCurrentUser() async {
    try {
      final response = await _apiService.get('/auth/me');
      if (response.statusCode == 200) {
        final user = User.fromJson(response.data);
        return user;
      } else {
        throw Exception('Failed to get user info');
      }
    } catch (e) {
      throw Exception(_apiService.handleError(e));
    }
  }

  Future<void> logout() async {
    try {
      await _googleSignIn.signOut();
      await _storageService.clearAll();
    } catch (e) {
      await _storageService.clearAll();
    }
  }

  Future<bool> isLoggedIn() async {
    return await _storageService.isLoggedIn();
  }
}
