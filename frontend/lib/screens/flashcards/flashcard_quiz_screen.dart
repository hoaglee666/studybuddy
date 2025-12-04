import 'package:flutter/material.dart';

class FlashcardQuizScreen extends StatefulWidget {
  const FlashcardQuizScreen({super.key});

  @override
  State<FlashcardQuizScreen> createState() => _FlashcardsScreenState();
}

class _FlashcardsScreenState extends State<FlashcardQuizScreen> {
  bool _showAnswer = false;
  int _currentIndex = 0;
  //sample
  final List<Map<String, String>> _flashcards = [
    {'question': 'What is the capital of France?', 'answer': 'Paris'},
    {'question': 'What is 2 + 2?', 'answer': '4'},
  ];

  void _flipCard() {
    setState(() {
      _showAnswer != _showAnswer;
    });
  }

  void _nextCard() {
    if (_currentIndex < _flashcards.length - 1) {
      setState(() {
        _currentIndex++;
        _showAnswer = false;
      });
    }
  }

  void _previousCard() {
    if (_currentIndex > 0) {
      setState(() {
        _currentIndex--;
        _showAnswer = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_flashcards.isEmpty) {
      return Scaffold(
        appBar: AppBar(title: const Text('Practice')),
        body: const Center(child: Text('No flashcards available')),
      );
    }
    final currentCard = _flashcards[_currentIndex];
    return Scaffold(
      appBar: AppBar(
        title: Text('Card ${_currentIndex + 1} of ${_flashcards.length}'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            //progs indica
            LinearProgressIndicator(
              value: (_currentIndex + 1) / _flashcards.length,
              backgroundColor: Colors.grey[200],
            ),
            const SizedBox(height: 32),
            //flashcard
            Expanded(
              child: GestureDetector(
                onTap: _flipCard,
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
                          _showAnswer
                              ? currentCard['answer']!
                              : currentCard['question']!,
                          style: Theme.of(context).textTheme.headlineMedium,
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 24),
                        Text(
                          'Tap to ${_showAnswer ? 'see question' : 'reveal_answer'}',
                          style: Theme.of(context).textTheme.bodySmall,
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 32),
            //nav butts
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton.icon(
                  onPressed: _currentIndex > 0 ? _previousCard : null,
                  icon: const Icon(Icons.arrow_back),
                  label: const Text('Previous'),
                  style: ElevatedButton.styleFrom(backgroundColor: Colors.grey),
                ),
                ElevatedButton.icon(
                  onPressed: _currentIndex < _flashcards.length - 1
                      ? _nextCard
                      : null,
                  icon: const Icon(Icons.arrow_forward),
                  label: const Text('Next'),
                ),
              ],
            ),
            //diff buts
            if (_showAnswer)
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  TextButton.icon(
                    onPressed: _nextCard,
                    icon: const Icon(Icons.check, color: Colors.green),
                    label: const Text('Hard'),
                    style: TextButton.styleFrom(foregroundColor: Colors.red),
                  ),
                  TextButton.icon(
                    onPressed: _nextCard,
                    icon: const Icon(Icons.check, color: Colors.green),
                    label: const Text('Easy'),
                    style: TextButton.styleFrom(foregroundColor: Colors.green),
                  ),
                ],
              ),
          ],
        ),
      ),
    );
  }
}
