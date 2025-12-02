class StudySession {
  final int id;
  final int userId;
  final int durationMinutes;
  final int notesReviewed;
  final int flashcardsPraticed;
  final String? subject;
  final String? sessionType;
  final DateTime createdAt;

  StudySession({
    required this.id,
    required this.userId,
    required this.durationMinutes,
    required this.notesReviewed,
    required this.flashcardsPraticed,
    this.subject,
    this.sessionType,
    required this.createdAt,
  });

  factory StudySession.fromJson(Map<String, dynamic> json) {
    return StudySession(
      id: json['id'],
      userId: json['user_id'],
      durationMinutes: json['duration_minutes'],
      notesReviewed: json['notes_reviewed'],
      flashcardsPraticed: json['flashcards_practiced'],
      subject: json['subject'],
      sessionType: json['session_type'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }
}
