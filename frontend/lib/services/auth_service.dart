import 'package:google_sign_in/google_sign_in.dart';
import '../models/user.dart';
import 'api_service.dart';
import 'storage_service.dart';

class AuthService {
  final ApiService _apiService = ApiService();
  final StorageService _storageService = StorageService();
  final GoogleSignIn _googleSignIn = GoogleSignIn(scopes: ['email', 'profile']);

  // Register with email and password
  Future<User> register(String email, String name, String password) async {
    try {
      final response = await _apiService.post(
        '/auth/register',
        data: {'email': email, 'name': name, 'password': password},
      );

      if (response.statusCode == 200) {
        // Save tokens
        await _storageService.saveTokens(
          response.data['access_token'],
          response.data['refresh_token'],
        );

        // Get user info
        return await getCurrentUser();
      } else {
        throw Exception('Registration failed');
      }
    } catch (e) {
      throw Exception(_apiService.handleError(e));
    }
  }

  // Login with email and password
  Future<User> login(String email, String password) async {
    try {
      final response = await _apiService.post(
        '/auth/login',
        data: {
          'username':
              email, // FastAPI OAuth2PasswordRequestForm uses 'username'
          'password': password,
        },
      );

      if (response.statusCode == 200) {
        // Save tokens
        await _storageService.saveTokens(
          response.data['access_token'],
          response.data['refresh_token'],
        );

        // Get user info
        return await getCurrentUser();
      } else {
        throw Exception('Login failed');
      }
    } catch (e) {
      throw Exception(_apiService.handleError(e));
    }
  }

  // Google Sign In
  Future<User> signInWithGoogle() async {
    try {
      final GoogleSignInAccount? googleUser = await _googleSignIn.signIn();
      if (googleUser == null) {
        throw Exception('Google sign in cancelled');
      }

      final GoogleSignInAuthentication googleAuth =
          await googleUser.authentication;

      // Send Google token to backend
      // Note: You'll need to implement this endpoint in your backend
      // For now, we'll use a simplified version
      throw Exception(
        'Google Sign In not fully implemented yet. Please use email/password.',
      );
    } catch (e) {
      throw Exception('Google sign in failed: ${e.toString()}');
    }
  }

  // Get current user
  Future<User> getCurrentUser() async {
    try {
      final response = await _apiService.get('/auth/me');
      if (response.statusCode == 200) {
        final user = User.fromJson(response.data);
        await _storageService.saveUser(user);
        return user;
      } else {
        throw Exception('Failed to get user info');
      }
    } catch (e) {
      throw Exception(_apiService.handleError(e));
    }
  }

  // Logout
  Future<void> logout() async {
    try {
      await _googleSignIn.signOut();
      await _storageService.clearAll();
    } catch (e) {
      // Always clear local data even if remote logout fails
      await _storageService.clearAll();
    }
  }

  // Check if logged in
  Future<bool> isLoggedIn() async {
    return await _storageService.isLoggedIn();
  }
}
