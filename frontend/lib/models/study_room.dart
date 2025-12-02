class StudyRoom {
  final String id;
  final String name;
  final String subject;
  final int activeUsers;

  StudyRoom({
    required this.id,
    required this.name,
    required this.subject,
    required this.activeUsers,
  });

  factory StudyRoom.fromJson(Map<String, dynamic> json) {
    return StudyRoom(
      id: json['id'],
      name: json['name'],
      subject: json['subject'],
      activeUsers: json['active_users'] ?? 0,
    );
  }
}
