class ChatMessage {
  final int id;
  final String roomId;
  final int userId;
  final String userName;
  final String message;
  final DateTime timestamp;

  ChatMessage({
    required this.id,
    required this.roomId,
    required this.userId,
    required this.userName,
    required this.message,
    required this.timestamp,
  });

  factory ChatMessage.fromJson(Map<String, dynamic> json) {
    return ChatMessage(
      id: json['id'],
      roomId: json['room_id'],
      userId: json['user_id'],
      userName: json['user_name'],
      message: json['message'],
      timestamp: DateTime.parse(json['timestamp']),
    );
  }
}
