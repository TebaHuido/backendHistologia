import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ApiService } from '../services/api.service';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-upload-xls',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './upload-xls.component.html',
  styleUrls: ['./upload-xls.component.css']
})
export class UploadXlsComponent implements OnInit {
  uploadForm: FormGroup;
  cursos: any[] = [];
  alumnos: any[] = [];

  constructor(
    private fb: FormBuilder,
    private apiService: ApiService,
    private authService: AuthService
  ) {
    this.uploadForm = this.fb.group({
      file: [null]
    });
  }

  ngOnInit(): void {
    this.loadCursos();
    this.loadAlumnos();
  }

  loadCursos(): void {
    const headers = this.authService.getAuthHeaders();
    this.apiService.getCursos(headers).subscribe(
      (response: any) => {
        this.cursos = response;
        console.log('Cursos loaded successfully', response);
      },
      (error: any) => {
        console.error('Error loading cursos', error);
      }
    );
  }

  loadAlumnos(): void {
    const headers = this.authService.getAuthHeaders();
    this.apiService.getAlumnos(headers).subscribe(
      (response: any) => {
        this.alumnos = response;
        console.log('Alumnos loaded successfully', response);
      },
      (error: any) => {
        console.error('Error loading alumnos', error);
      }
    );
  }

  onFileChange(event: any) {
    const file = event.target.files[0];
    this.uploadForm.patchValue({
      file: file
    });
  }

  onSubmit() {
    const file = this.uploadForm.get('file')?.value;
    if (file) {
      let headers = this.authService.getAuthHeaders();
      const csrfToken = this.authService.getCSRFToken();
      if (csrfToken) {
        headers = headers.set('X-CSRFToken', csrfToken); // Ensure CSRF token is set correctly
      } else {
        console.error('CSRF token not found.');
        return;
      }

      this.apiService.uploadXls(file, headers).subscribe(response => {
        console.log('File uploaded successfully', response);
      }, error => {
        if (error.status === 403 && error.error.code === 'token_not_valid') {
          this.authService.refreshToken().subscribe({
            next: (response: any) => {
              this.authService.setToken(response.access);
              this.onSubmit(); // Retry the request with the new token
            },
            error: refreshErr => {
              console.error('Error al refrescar el token:', refreshErr);
              this.authService.logout();
            }
          });
        } else {
          console.error('Error uploading file', error);
        }
      });
    }
  }
}
