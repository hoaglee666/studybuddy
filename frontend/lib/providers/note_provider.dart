import 'package:flutter/material.dart';
import 'package:studybuddy/models/note.dart';
import 'package:studybuddy/services/note_service.dart';

class NoteProvider with ChangeNotifier {
  final NoteService _noteService = NoteService();

  List<Note> _notes = [];
  bool _isLoading = false;
  String? _error;
  int _currentPage = 1;
  int _totalPages = 1;
  int _total = 0;

  List<Note> get notes => _notes;
  bool get isLoading => _isLoading;
  String? get error => _error;
  int get currentPage => _currentPage;
  int get totalPages => _totalPages;
  int get total => _total;

  Future<void> loadNotes({
    int page = 1,
    String? search,
    String? subject,
  }) async {
    _isLoading = true;
    _error = null;
    notifyListeners();
    try {
      final result = await _noteService.getNotes(
        page: page,
        search: search,
        subject: subject,
      );
      _notes = result['notes'];
      _currentPage = result['page'];
      _totalPages = result['total_pages'];
      _total = result['total'];
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<bool> createNote({
    required String title,
    required String content,
    String? tags,
    String? subject,
  }) async {
    try {
      final note = await _noteService.createNote(
        title: title,
        content: content,
        tags: tags,
        subject: subject,
      );
      _notes.insert(0, note);
      _total++;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString();
      notifyListeners();
      return false;
    }
  }

  Future<bool> updateNote(
    int id, {
    String? title,
    String? content,
    String? tags,
    String? subject,
  }) async {
    try {
      final updatedNote = await _noteService.updateNote(
        id,
        title: title,
        content: content,
        tags: tags,
        subject: subject,
      );
      final index = _notes.indexWhere((n) => n.id == id);
      if (index != -1) {
        _notes[index] = updatedNote;
        notifyListeners();
      }
      return true;
    } catch (e) {
      _error = e.toString();
      notifyListeners();
      return false;
    }
  }

  Future<bool> deleteNote(int id) async {
    try {
      await _noteService.deleteNote(id);
      _notes.removeWhere((n) => n.id == id);
      _total--;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString();
      notifyListeners();
      return false;
    }
  }

  Future<String?> uploadImage(int noteId, String imagePath) async {
    try {
      final imageUrl = await _noteService.uploadImage(noteId, imagePath);
      return imageUrl;
    } catch (e) {
      _error = e.toString();
      notifyListeners();
      return null;
    }
  }

  void clearError() {
    _error = null;
    notifyListeners();
  }
}
