import { Component, OnInit } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, FormGroup, FormArray, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  standalone: true,
  selector: 'app-uplimage',
  templateUrl: './uplimage.component.html',
  styleUrls: ['./uplimage.component.css'],
  imports: [ReactiveFormsModule, CommonModule]
})
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
      name: ['', Validators.required],
      category: ['', Validators.required],
      newCategory: [''],
      organo: ['', Validators.required],
      newOrgano: [''],
      sistema: ['', Validators.required],
      newSistema: [''],
      images: this.fb.array([], Validators.required) // Validación para asegurar que se suban imágenes
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
  }

  onOrganoChange(event: any) {
    const value = event.target.value;
    this.isCreatingNewOrgano = value === 'new';
  }

  onSistemaChange(event: any) {
    const value = event.target.value;
    this.isCreatingNewSistema = value === 'new';
  }

  onFileChange(event: any) {
    const files = event.target.files;
    if (files.length > 0) {
      this.selectedFiles = Array.from(files);
      this.imageFormArray.clear();
      this.selectedFiles.forEach(() => this.imageFormArray.push(this.fb.control('')));
    }
  }

  get imageFormArray(): FormArray {
    return this.sampleForm.get('images') as FormArray;
  }

  onSubmit() {
    if (this.sampleForm.invalid) {
      console.error('Formulario inválido:', this.sampleForm.errors);
      return;
    }
  
    const formData = new FormData();
    formData.append('name', this.sampleForm.get('name')?.value);
  
    // Asegurarse de que `categoria` siempre sea una lista
    const selectedCategory = this.sampleForm.get('category')?.value;
    const newCategory = this.sampleForm.get('newCategory')?.value;
  
    if (this.isCreatingNewCategory && newCategory) {
      formData.append('categoria', newCategory); // Agregar nueva categoría como lista
    } else if (selectedCategory) {
      formData.append('categoria', selectedCategory); // Agregar categoría seleccionada como lista
    } else {
      formData.append('categoria', '') // Enviar lista vacía si no hay selección
    }
  
    // Manejo de órganos (también en formato de lista)
    const selectedOrgano = this.sampleForm.get('organo')?.value;
    const newOrgano = this.sampleForm.get('newOrgano')?.value;
  
    if (this.isCreatingNewOrgano && newOrgano) {
      formData.append('organo', newOrgano);
    } else if (selectedOrgano) {
      formData.append('organo', selectedOrgano);
    } else {
      formData.append('organo', '');
    }
  
    // Manejo de imágenes
    this.selectedFiles.forEach((file, index) => {
      formData.append('images', file);
      formData.append('image_names', this.imageFormArray.at(index).value || '');
    });
  
    // Enviar solicitud al servidor
    this.http.post('http://localhost:8000/muestras/', formData).subscribe({
      next: (response) => {
        console.log('Muestra creada exitosamente:', response);
        this.resetForm();
      },
      error: (err) => {
        console.error('Error al crear la muestra:', err);
      }
    });
  }

  resetForm() {
    this.sampleForm.reset();
    this.selectedFiles = [];
    this.imageFormArray.clear();
    this.isCreatingNewCategory = false;
    this.isCreatingNewOrgano = false;
    this.isCreatingNewSistema = false;
  }
}
