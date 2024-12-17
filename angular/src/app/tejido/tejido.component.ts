import { Component, OnInit } from '@angular/core';
import { NgFor, CommonModule } from '@angular/common'; // Import CommonModule
import { FormsModule } from '@angular/forms'; // Import FormsModule
import { HttpHeaders } from '@angular/common/http'; // Import HttpHeaders
import { ApiService } from '../services/api.service';
import { Muestra, Tejido } from '../services/tejidos.mock';
import { ActivatedRoute } from '@angular/router';
import { NgxImageZoomModule } from 'ngx-image-zoom';
import { ImagenZoomComponent } from '../imagen-zoom/imagen-zoom.component';
import { AuthService } from '../services/auth.service';
import { SharedModule } from '../shared/shared.module'; // Import SharedModule

interface Nota {
  id?: number;
  titulo: string;
  cuerpo: string;
  alumno?: number;
  profesor?: number;
}

@Component({
  selector: 'app-tejido',
  standalone: true,
  imports: [NgFor, CommonModule, FormsModule, NgxImageZoomModule, ImagenZoomComponent, SharedModule], // Add SharedModule to imports
  templateUrl: './tejido.component.html',
  styleUrls: ['./tejido.component.css']
})
export class TejidoComponent implements OnInit {
  tejidosArray: Muestra[] = [];
  imagenSeleccionada: { image: string } | undefined;
  initialLabels: { x: number; y: number }[] = [];
  isSidebarCollapsed = false;
  newNota: Nota = { titulo: '', cuerpo: '' }; // Elimina el campo muestra
  isEditingNota = false;
  isLoading = false;
  errorMessage = '';

  constructor(private route: ActivatedRoute, private api: ApiService, public auth: AuthService) { }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      const id = params.get('id');
      if (id) {
        this.getTejido(parseInt(id, 10));
      }
    });
  }

  getTejido(id: number): void {
    this.isLoading = true;
    this.errorMessage = '';
    const headers = this.auth.getAuthHeaders();
    this.api.getTejido(id, headers).subscribe({
      next: (tejido: Tejido) => {
        const muestra: Muestra = {
          id: tejido.id,
          name: tejido.name,
          capturas: tejido.capturas,
          notas: tejido.notas.map(nota => ({
            ...nota,
            titulo: nota.titulo || 'Sin título',
            cuerpo: nota.cuerpo || ''
          })),
          sistemas: tejido.sistemas.map((s: any) => `${s.sistema} - ${s.organo}`)
        };
        this.tejidosArray.push(muestra);
        if (muestra.capturas && muestra.capturas.length > 0) {
          const originalUrl = muestra.capturas[0].image;
          this.imagenSeleccionada = { image: originalUrl };
        } else {
          console.warn('No se encontraron capturas en el tejido.');
        }
        this.isLoading = false;
      },
      error: (err: any) => {
        this.isLoading = false;
        if (err.status === 403 && err.error.code === 'token_not_valid') {
          this.auth.refreshToken().subscribe({
            next: (response: any) => {
              this.auth.setToken(response.access);
              this.getTejido(id);
            },
            error: refreshErr => {
              console.error('Error al refrescar el token:', refreshErr);
              this.auth.logout();
            }
          });
        } else if (err.status === 404) {
          this.errorMessage = 'Tejido no encontrado.';
          console.error('Tejido no encontrado:', err);
        } else {
          this.errorMessage = 'Error al obtener el tejido.';
          console.error('Error al obtener el tejido:', err);
        }
      }
    });
  }

  seleccionarImagen(captura: { image: string }): void {
    this.imagenSeleccionada = { image: captura.image };
  }

  selectCategory(category: string) {
    console.log('Categoría seleccionada:', category);
  }

  toggleSidebar(): void {
    this.isSidebarCollapsed = !this.isSidebarCollapsed;
  }

  startAddNota(): void {
    this.isEditingNota = true;
    this.newNota = { titulo: '', cuerpo: '' }; // Elimina el campo muestra
  }

  editNota(nota: Nota): void {
    this.isEditingNota = true;
    this.newNota = { ...nota };
  }

  saveNota(): void {
    const user = this.auth.getUser();
    if (!user) {
      console.error('No se encontró el usuario.');
      return;
    }

    if (user.is_alumno) {
      this.newNota.alumno = user.id;
    } else if (user.is_profesor) {
      this.newNota.profesor = user.id;
    } else {
      console.error('El usuario debe ser un alumno o un profesor.');
      return;
    }

    let headers = this.auth.getAuthHeaders();
    const csrfToken = this.auth.getCSRFToken();
    if (csrfToken) {
      headers = headers.set('X-CSRFToken', csrfToken); // Ensure CSRF token is set correctly
    } else {
      console.error('CSRF token not found.');
      return;
    }

    const notaData = {
      titulo: this.newNota.titulo,
      cuerpo: this.newNota.cuerpo,
      alumno: this.newNota.alumno,
      profesor: this.newNota.profesor,
      muestra: this.tejidosArray[0]?.id // Asegúrate de que la nota pertenezca a una muestra
    };
    console.log('Request data:', notaData); // Log the request data

    if (this.newNota.id) {
      this.api.updateNota(this.newNota.id, { nota: notaData }, headers).subscribe({
        next: (response: any) => {
          console.log('Nota actualizada exitosamente:', response);
          const index = this.tejidosArray[0].notas.findIndex(n => n.id === this.newNota.id);
          if (index !== -1) {
            this.tejidosArray[0].notas[index] = response;
          }
          this.newNota = { titulo: '', cuerpo: '' };
          this.isEditingNota = false;
        },
        error: (err: any) => {
          console.error('Error al actualizar la nota:', err);
        }
      });
    } else {
      this.api.addNota({ nota: notaData }, headers, { withCredentials: true }).subscribe({
        next: (response: any) => {
          console.log('Nota agregada exitosamente:', response);
          this.tejidosArray[0].notas.push(response);
          this.newNota = { titulo: '', cuerpo: '' };
          this.isEditingNota = false;
        },
        error: (err: any) => {
          console.error('Error al agregar la nota:', err);
          if (err.status === 403) {
            console.error('Error 403: Forbidden. Verifica los permisos y la autenticación.');
          }
        }
      });
    }
  }

  getAuthHeaders(): HttpHeaders {
    const token = this.auth.getToken();
    let headers = new HttpHeaders();
    if (token) {
      headers = headers.set('Authorization', `Bearer ${token}`);
    }
    return headers;
  }

  getCSRFToken(): string | null {
    const csrfCookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
    if (!csrfCookie) {
      console.error('CSRF cookie not set.');
      return null;
    }
    return csrfCookie.split('=')[1];
  }
}

