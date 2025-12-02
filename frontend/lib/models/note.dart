class Note {
  final int id;
  final int userId;
  final String title;
  final String content;
  final String? tags;
  final String? subject;
  final String? imageUrl;
  final DateTime createdAt;
  final DateTime? updatedAt;

  Note({
    required this.id,
    required this.userId,
    required this.title,
    required this.content,
    this.tags,
    this.subject,
    this.imageUrl,
    required this.createdAt,
    this.updatedAt,
  });

  factory Note.fromJson(Map<String, dynamic> json) {
    return Note(
      id: json['id'],
      userId: json['user_id'],
      title: json['title'],
      content: json['content'],
      tags: json['tags'],
      subject: json['subject'],
      imageUrl: json['image_url'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: json['updated_at'] != null
          ? DateTime.parse(json['updated_at'])
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'title': title,
      'content': content,
      'tags': tags,
      'subject': subject,
    };
  }
}
