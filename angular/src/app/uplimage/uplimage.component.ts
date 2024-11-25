// uplimage.component.ts

import { Component, OnInit } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, FormGroup, FormArray } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
@Component({
  standalone: true,
  selector: 'app-uplimage',
  templateUrl: './uplimage.component.html',
  styleUrls: ['./uplimage.component.css'],
  imports: [ReactiveFormsModule, CommonModule]
})
// uplimage.component.ts
export class UplimageComponent implements OnInit {
  sampleForm: FormGroup;
  categories: any[] = [];
  organos: any[] = [];
  sistemas: any[] = [];
  isCreatingNewCategory = false;
  isCreatingNewOrgano = false;
  isCreatingNewSistema = false;
  selectedFiles: File[] = [];

  constructor(private fb: FormBuilder, private http: HttpClient) {
    this.sampleForm = this.fb.group({
      name: [''],
      category: [''],
      newCategory: [''],
      organo: [''],
      newOrgano: [''],
      sistema: [''],
      newSistema: [''],
      images: this.fb.array([])
    });
  }

  ngOnInit() {
    this.loadCategories();
    this.loadOrganos();
    this.loadSistemas();
  }

  loadCategories() {
    this.http.get('http://localhost:8000/categorias/').subscribe((data: any) => {
      this.categories = data;
    });
  }

  loadOrganos() {
    this.http.get('http://localhost:8000/organos/').subscribe((data: any) => {
      this.organos = data;
    });
  }

  loadSistemas() {
    this.http.get('http://localhost:8000/sistemas/').subscribe((data: any) => {
      this.sistemas = data;
    });
  }

  onCategoryChange(event: any) {
    const value = event.target.value;
    this.isCreatingNewCategory = value === 'new';
    if (this.isCreatingNewCategory) {
      this.sampleForm.get('newCategory')?.setValue('');
    } else {
      this.sampleForm.get('newCategory')?.setValue('');
    }
  }

  onOrganoChange(event: any) {
    const value = event.target.value;
    this.isCreatingNewOrgano = value === 'new';
    if (this.isCreatingNewOrgano) {
      this.sampleForm.get('newOrgano')?.setValue('');
    } else {
      this.sampleForm.get('newOrgano')?.setValue('');
    }
  }

  onSistemaChange(event: any) {
    const value = event.target.value;
    this.isCreatingNewSistema = value === 'new';
    if (this.isCreatingNewSistema) {
      this.sampleForm.get('newSistema')?.setValue('');
    } else {
      this.sampleForm.get('newSistema')?.setValue('');
    }
  }

  onFileChange(event: any) {
    const files = event.target.files;
    if (files.length > 0) {
      this.selectedFiles = [];
      this.imageFormArray.clear();
      for (let i = 0; i < files.length; i++) {
        this.selectedFiles.push(files[i]);
        this.imageFormArray.push(this.fb.control(''));
      }
    }
  }

  get imageFormArray(): FormArray {
    return this.sampleForm.get('images') as FormArray;
  }

  onSubmit() {
    if (this.sampleForm.invalid) {
      return;
    }

    const formData = new FormData();
    formData.append('name', this.sampleForm.get('name')?.value);

    // Manejo de categorías
    const selectedCategory = this.sampleForm.get('category')?.value;
    if (this.isCreatingNewCategory) {
      formData.append('new_category', this.sampleForm.get('newCategory')?.value);
    } else if (selectedCategory && selectedCategory !== 'new') {
      formData.append('Categoria', selectedCategory.toString());
    }

    // Manejo de órganos
    const selectedOrgano = this.sampleForm.get('organo')?.value;
    if (this.isCreatingNewOrgano) {
      formData.append('new_organo', this.sampleForm.get('newOrgano')?.value);

      // Manejo de sistemas al crear un nuevo órgano
      const selectedSistema = this.sampleForm.get('sistema')?.value;
      if (this.isCreatingNewSistema) {
        formData.append('new_sistema', this.sampleForm.get('newSistema')?.value);
      } else if (selectedSistema && selectedSistema !== 'new') {
        formData.append('Sistema', selectedSistema.toString());
      }
    } else if (selectedOrgano && selectedOrgano !== 'new') {
      formData.append('Organo', selectedOrgano.toString());
    }

    // Agregar archivos de imagen y sus nombres
    for (let i = 0; i < this.selectedFiles.length; i++) {
      formData.append('images', this.selectedFiles[i]);
      formData.append('image_names', this.imageFormArray.at(i).value);
    }

    // Hacer la solicitud POST al servidor
    this.http.post('http://localhost:8000/muestras/', formData).subscribe(
      response => {
        console.log('Muestra creada exitosamente', response);
        this.sampleForm.reset();
        this.selectedFiles = [];
        this.imageFormArray.clear();
        this.isCreatingNewCategory = false;
        this.isCreatingNewOrgano = false;
        this.isCreatingNewSistema = false;
      },
      error => {
        console.error('Error al crear la muestra', error);
      }
    );
  }
}