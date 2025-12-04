import 'package:flutter/material.dart';
import 'package:studybuddy/models/flashcard.dart';

class FlashcardWidget extends StatefulWidget {
  final Flashcard flashcard;
  final VoidCallback? onCorrect;
  final VoidCallback? onIncorrect;

  const FlashcardWidget({
    super.key,
    required this.flashcard,
    this.onCorrect,
    this.onIncorrect,
  });

  @override
  State<FlashcardWidget> createState() => _FlashcardWidgetState();
}

class _FlashcardWidgetState extends State<FlashcardWidget> {
  bool _showAnswer = false;

  void _flip() {
    setState(() {
      _showAnswer = !_showAnswer;
    });
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: _flip,
      child: Card(
        elevation: 8,
        child: Container(
          width: double.infinity,
          padding: const EdgeInsets.all(32),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                _showAnswer ? Icons.lightbulb : Icons.help_outline,
                size: 48,
                color: const Color(0xff6366f1),
              ),
              const SizedBox(height: 24),
              Text(
                _showAnswer ? 'Answer' : 'Question',
                style: Theme.of(
                  context,
                ).textTheme.titleMedium?.copyWith(color: Colors.grey),
              ),
              const SizedBox(height: 16),
              Text(
                _showAnswer
                    ? widget.flashcard.answer
                    : widget.flashcard.question,
                style: Theme.of(context).textTheme.headlineMedium,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 24),
              Text(
                'Tap to ${_showAnswer ? 'see question' : 'reveal answer'}',
                style: Theme.of(context).textTheme.bodySmall,
              ),
              if (_showAnswer &&
                  (widget.onCorrect != null || widget.onIncorrect != null)) ...[
                const SizedBox(height: 32),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    if (widget.onIncorrect != null)
                      ElevatedButton.icon(
                        onPressed: widget.onIncorrect,
                        icon: const Icon(Icons.close),
                        label: const Text('Incorrect'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.red,
                        ),
                      ),
                    if (widget.onCorrect != null)
                      ElevatedButton.icon(
                        onPressed: widget.onCorrect,
                        icon: const Icon(Icons.check),
                        label: const Text('Correct'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.green,
                        ),
                      ),
                  ],
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}
