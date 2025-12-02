class Flashcard {
  final int id;
  final int userId;
  final String question;
  final String answer;
  final String? subject;
  final String difficulty;
  final int timesReviewed;
  final int timesCorrect;
  final DateTime? nextReview;
  final DateTime createdAt;

  Flashcard({
    required this.id,
    required this.userId,
    required this.question,
    required this.answer,
    this.subject,
    required this.difficulty,
    required this.timesReviewed,
    required this.timesCorrect,
    this.nextReview,
    required this.createdAt,
  });

  factory Flashcard.fromJson(Map<String, dynamic> json) {
    return Flashcard(
      id: json['id'],
      userId: json['user_id'],
      question: json['question'],
      answer: json['answer'],
      subject: json['subject'],
      difficulty: json['difficulty'],
      timesReviewed: json['times_reviewed'],
      timesCorrect: json['times_correct'],
      nextReview: json['next_review'] != null
          ? DateTime.parse(json['next_review'])
          : null,
      createdAt: DateTime.parse(json['created_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'question': question,
      'answer': answer,
      'subject': subject,
      'difficulty': difficulty,
    };
  }

  double get accuracy {
    if (timesReviewed == 0) return 0;
    return (timesCorrect / timesReviewed) * 100;
  }
}
