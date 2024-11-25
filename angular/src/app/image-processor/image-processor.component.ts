import { Component, OnDestroy } from '@angular/core';
import { HttpClient, HttpEventType, HttpErrorResponse } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ImagenZoomComponent } from '../imagen-zoom/imagen-zoom.component';

@Component({
  selector: 'app-image-processor',
  standalone: true,
  templateUrl: './image-processor.component.html',
  styleUrls: ['./image-processor.component.css'],
  imports: [CommonModule, FormsModule, ImagenZoomComponent]
})
export class ImageProcessorComponent implements OnDestroy {
  selectedFile: File | null = null;
  previewImageUrl: string | null = null;
  processedImageUrl: string | null = null;
  uploadProgress: number = 0;
  errorMessage: string = '';
  successMessage: string = '';
  isLoading: boolean = false;

  scaleFactor: number = 1.01;
  minNeighbors: number = 5;
  minSize: [number, number] = [5, 5];
  maxSize: [number, number] = [500, 500];
  shrinkFactor: number = 0.85;

  constructor(private http: HttpClient) {}

  onFileSelected(event: any): void {
    const file: File = event.target.files[0];
    if (file) {
      this.selectedFile = file;
      this.previewImageUrl = URL.createObjectURL(file);
      this.resetProgress();
    }
  }

  applyParameters(): void {
    if (!this.selectedFile) {
      this.errorMessage = 'Por favor, selecciona una imagen primero.';
      return;
    }
    if (this.validateParameters()) {
      this.uploadImage();
    } else {
      this.errorMessage = 'Revisa los parámetros antes de procesar.';
    }
  }

  validateParameters(): boolean {
    return (
      this.scaleFactor >= 1.01 && this.scaleFactor <= 2.0 &&
      this.minNeighbors >= 1 && this.minNeighbors <= 10 &&
      this.shrinkFactor >= 0.5 && this.shrinkFactor <= 1.0 &&
      this.minSize[0] > 0 && this.minSize[1] > 0 &&
      this.maxSize[0] > 0 && this.maxSize[1] > 0 &&
      this.maxSize[0] >= this.minSize[0] &&
      this.maxSize[1] >= this.minSize[1]
    );
  }

  uploadImage(): void {
    if (!this.selectedFile) return;

    const formData = new FormData();
    formData.append('imagen', this.selectedFile);
    formData.append('scaleFactor', this.scaleFactor.toString());
    formData.append('minNeighbors', this.minNeighbors.toString());
    formData.append('minSize', `${this.minSize[0]},${this.minSize[1]}`);
    formData.append('maxSize', `${this.maxSize[0]},${this.maxSize[1]}`);
    formData.append('shrink_factor', this.shrinkFactor.toString());

    const apiEndpoint = 'http://localhost:8000/procesar-imagen/';
    this.isLoading = true;

    this.http.post(apiEndpoint, formData, {
      reportProgress: true,
      observe: 'events',
      responseType: 'blob'
    }).subscribe({
      next: event => {
        if (event.type === HttpEventType.UploadProgress && event.total) {
          this.uploadProgress = Math.round((100 * event.loaded) / event.total);
        } else if (event.type === HttpEventType.Response && event.body) {
          this.processedImageUrl = URL.createObjectURL(event.body);
          this.successMessage = 'Imagen procesada correctamente.';
        }
      },
      error: (err: HttpErrorResponse) => {
        this.errorMessage = err.error?.error ?? 'Hubo un error al procesar la imagen.';
      },
      complete: () => this.isLoading = false
    });
  }

  retryUpload(): void {
    this.errorMessage = '';
    this.uploadImage();
  }

  resetProgress(): void {
    this.uploadProgress = 0;
    this.processedImageUrl = null;
    this.errorMessage = '';
    this.successMessage = '';
  }

  ngOnDestroy(): void {
    if (this.previewImageUrl) URL.revokeObjectURL(this.previewImageUrl);
    if (this.processedImageUrl) URL.revokeObjectURL(this.processedImageUrl);
  }
}
