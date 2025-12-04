import 'package:studybuddy/models/note.dart';
import 'package:studybuddy/services/api_service.dart';

class NoteService {
  final ApiService _apiService = ApiService();

  Future<Note> createNote({
    required String title,
    required String content,
    String? tags,
    String? subject,
  }) async {
    try {
      final response = await _apiService.post(
        '/notes/',
        data: {
          'title': title,
          'content': content,
          'tags': tags,
          'subject': subject,
        },
      );
      if (response.statusCode == 201) {
        return Note.fromJson(response.data);
      } else {
        throw Exception('Failed to create note');
      }
    } catch (e) {
      throw Exception(_apiService.handleError(e));
    }
  }

  Future<Map<String, dynamic>> getNotes({
    int page = 1,
    int pageSize = 10,
    String? search,
    String? subject,
    String sortBy = 'created_at',
    String sortOrder = 'desc',
  }) async {
    try {
      final response = await _apiService.get(
        '/notes/',
        queryParameters: {
          'page': page,
          'page_size': pageSize,
          if (search != null) 'search': search,
          if (subject != null) 'subject': subject,
          'sort_by': sortBy,
          'sort_order': sortOrder,
        },
      );
      if (response.statusCode == 200) {
        return {
          'notes': (response.data['notes'] as List)
              .map((note) => Note.fromJson(note))
              .toList(),
          'total': response.data['total'],
          'page': response.data['page'],
          'page_size': response.data['page_size'],
          'total_pages': response.data['total_pages'],
        };
      } else {
        throw Exception('Failed to load notes');
      }
    } catch (e) {
      throw Exception(_apiService.handleError(e));
    }
  }

  //get 1 note
  Future<Note> getNote(int id) async {
    try {
      final response = await _apiService.get('/notes/$id');
      if (response.statusCode == 200) {
        return Note.fromJson(response.data);
      } else {
        throw Exception('Failed to load note');
      }
    } catch (e) {
      throw Exception(_apiService.handleError(e));
    }
  }

  Future<Note> updateNote(
    int id, {
    String? title,
    String? content,
    String? tags,
    String? subject,
  }) async {
    try {
      final data = <String, dynamic>{};
      if (title != null) data['title'] = title;
      if (content != null) data['content'] = content;
      if (tags != null) data['tags'] = tags;
      if (subject != null) data['subject'] = subject;

      final response = await _apiService.put('/notes/$id', data: data);
      if (response.statusCode == 200) {
        return Note.fromJson(response.data);
      } else {
        throw Exception('Failed to update note');
      }
    } catch (e) {
      throw Exception(_apiService.handleError(e));
    }
  }

  Future<void> deleteNote(int id) async {
    try {
      final response = await _apiService.delete('/notes/$id');
      if (response.statusCode != 204) {
        throw Exception('Failed to delete note');
      }
    } catch (e) {
      throw Exception(_apiService.handleError(e));
    }
  }

  Future<String> uploadImage(int noteId, String imagePath) async {
    try {
      final response = await _apiService.uploadFile(
        '/notes/$noteId/upload-image',
        imagePath,
        fieldName: 'file',
      );
      if (response.statusCode == 200) {
        return response.data['image_url'];
      } else {
        throw Exception('Failed to upload image');
      }
    } catch (e) {
      throw Exception(_apiService.handleError(e));
    }
  }

  //get subj list
  Future<List<String>> getSubjects() async {
    try {
      final response = await _apiService.get('/notes/subjects/list');
      if (response.statusCode == 200) {
        return List<String>.from(response.data['subjects']);
      } else {
        throw Exception('Failed to load subjects');
      }
    } catch (e) {
      throw Exception(_apiService.handleError(e));
    }
  }
}
