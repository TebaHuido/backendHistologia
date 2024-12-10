import { Component, OnInit } from '@angular/core';
import { NgFor } from '@angular/common';
import { ApiService } from '../services/api.service';
import { Muestra, Tejido } from '../services/tejidos.mock';
import { ActivatedRoute } from '@angular/router';
import { NgxImageZoomModule } from 'ngx-image-zoom';
import { ImagenZoomComponent } from '../imagen-zoom/imagen-zoom.component';

@Component({
  selector: 'app-tejido',
  standalone: true,
  imports: [NgFor, NgxImageZoomModule, ImagenZoomComponent],
  templateUrl: './tejido.component.html',
  styleUrls: ['./tejido.component.css']
})
export class TejidoComponent implements OnInit {
  tejidosArray: Muestra[] = [];
  imagenSeleccionada: { image: string } | undefined;
  initialLabels: { x: number; y: number }[] = [];

  constructor(private route: ActivatedRoute, private api: ApiService) { }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      const id = params.get('id');
      if (id) {
        this.getTejido(parseInt(id, 10));
      }
    });
  }

  getTejido(id: number): void {
    this.api.getTejido(id).subscribe({
      next: (tejido: Tejido) => {
        const muestra: Muestra = {
          id: tejido.id,
          name: tejido.name,
          capturas: tejido.capturas,
          notas: tejido.notas,
          sistemas: tejido.sistemas
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
        console.error('Error al obtener el tejido:', err);
      }
    });
  }

  seleccionarImagen(captura: { image: string }): void {
    this.imagenSeleccionada = { image: captura.image };
  }

  selectCategory(arg0: string) {
    // Implementa la lógica para seleccionar categorías (notas, sistemas, etc.)
  }
}
