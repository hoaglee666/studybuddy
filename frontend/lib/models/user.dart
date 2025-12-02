class User {
  final int id;
  final String email;
  final String name;
  final String? profileImage;
  final String role;
  final String? oauthProvider;
  final DateTime createdAt;

  User({
    required this.id,
    required this.email,
    required this.name,
    this.profileImage,
    required this.role,
    this.oauthProvider,
    required this.createdAt,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      email: json['email'],
      name: json['name'],
      profileImage: json['profile_image'],
      role: json['role'],
      oauthProvider: json['oauth_provider'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'name': name,
      'profile_image': profileImage,
      'role': role,
      'oauth_provider': oauthProvider,
      'created_at': createdAt.toIso8601String(),
    };
  }
}
