import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

class ChatBubbleData {
  final String message;
  final bool isUser;
  final DateTime timestamp;

  ChatBubbleData({
    required this.message,
    required this.isUser,
    required this.timestamp,
  });
}

class ChatBubble extends StatelessWidget {
  final ChatBubbleData data;
  const ChatBubble({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Row(
        mainAxisAlignment: data.isUser
            ? MainAxisAlignment.end
            : MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (!data.isUser) ...[
            CircleAvatar(
              backgroundColor: const Color(0xff8b5cf6),
              radius: 16,
              child: const Icon(
                Icons.psychology,
                size: 16,
                color: Colors.white,
              ),
            ),
            const SizedBox(width: 8),
          ],
          Flexible(
            child: Column(
              crossAxisAlignment: data.isUser
                  ? CrossAxisAlignment.end
                  : CrossAxisAlignment.start,
              children: [
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: data.isUser
                        ? const Color(0xff6366f1)
                        : Colors.grey[200],
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Text(
                    data.message,
                    style: TextStyle(
                      color: data.isUser ? Colors.white : Colors.black87,
                    ),
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  DateFormat.jm().format(data.timestamp),
                  style: Theme.of(context).textTheme.bodySmall,
                ),
              ],
            ),
          ),
          if (data.isUser) ...[
            const SizedBox(width: 8),
            CircleAvatar(
              backgroundColor: const Color(0xff6366f1),
              radius: 16,
              child: const Icon(Icons.person, size: 16, color: Colors.white),
            ),
          ],
        ],
      ),
    );
  }
}
