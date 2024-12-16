import { Component, OnInit } from '@angular/core';
import { NgFor } from '@angular/common';
import { FormsModule } from '@angular/forms'; // Import FormsModule
import { ApiService } from '../services/api.service';
import { Muestra, Tejido } from '../services/tejidos.mock';
import { ActivatedRoute } from '@angular/router';
import { NgxImageZoomModule } from 'ngx-image-zoom';
import { ImagenZoomComponent } from '../imagen-zoom/imagen-zoom.component';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-tejido',
  standalone: true,
  imports: [NgFor, FormsModule, NgxImageZoomModule, ImagenZoomComponent], // Add FormsModule to imports
  templateUrl: './tejido.component.html',
  styleUrls: ['./tejido.component.css']
})
export class TejidoComponent implements OnInit {
  tejidosArray: Muestra[] = [];
  imagenSeleccionada: { image: string } | undefined;
  initialLabels: { x: number; y: number }[] = [];
  isSidebarCollapsed = false;
  newNota: string = '';

  constructor(private route: ActivatedRoute, private api: ApiService, private auth: AuthService) { }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      const id = params.get('id');
      if (id) {
        this.getTejido(parseInt(id, 10));
      }
    });
  }

  getTejido(id: number): void {
    const headers = this.auth.getAuthHeaders();
    this.api.getTejido(id, headers).subscribe({
      next: (tejido: Tejido) => {
        const muestra: Muestra = {
          id: tejido.id,
          name: tejido.name,
          capturas: tejido.capturas,
          notas: tejido.notas,
          sistemas: tejido.sistemas.map((s: any) => `${s.sistema} - ${s.organo}`)
        };
        this.tejidosArray.push(muestra);
        if (muestra.capturas && muestra.capturas.length > 0) {
          const originalUrl = muestra.capturas[0].image;
          this.imagenSeleccionada = { image: originalUrl };
        } else {
          console.warn('No se encontraron capturas en el tejido.');
        }
      },
      error: (err: any) => {
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
          console.error('Tejido no encontrado:', err);
        } else {
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

  addNota(): void {
    const user = this.auth.getUser();
    if (!user) {
      console.error('No se encontró el usuario.');
      return;
    }

    const nota = {
      nota: this.newNota,
      alumno: user.id,
      muestra: this.tejidosArray[0].id
    };

    const headers = this.auth.getAuthHeaders();
    this.api.addNota(nota, headers).subscribe({
      next: (response: any) => {
        console.log('Nota agregada exitosamente:', response);
        this.tejidosArray[0].notas.push(response);
        this.newNota = '';
      },
      error: (err: any) => {
        console.error('Error al agregar la nota:', err);
      }
    });
  }
}
