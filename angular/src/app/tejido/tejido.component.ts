import { Component, OnInit } from '@angular/core';
import { NgFor } from '@angular/common';
import { ApiService } from '../services/api.service';
import { Muestra } from '../services/tejidos.mock';
import { ActivatedRoute } from '@angular/router';
import { NgxImageZoomModule } from 'ngx-image-zoom';
import { ImagenZoomComponent } from '../imagen-zoom/imagen-zoom.component';
@Component({
  selector: 'app-tejido',
  standalone: true,
  imports: [NgFor,NgxImageZoomModule,ImagenZoomComponent],
  templateUrl: './tejido.component.html',
  styleUrls: ['./tejido.component.css']  // Cambié styleUrl a styleUrls
})
export class TejidoComponent implements OnInit {
  tejidosArray: Muestra[] = [];
  imagenSeleccionada: { image: string } | undefined;

  constructor(private route: ActivatedRoute, private api: ApiService) { }
  imageUrl = 'http://localhost:8011/images/f4147446-5ef3-4268-9296-bd1d86f29bb2.jpg';
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
      next: (tejido: Muestra) => {
        this.tejidosArray.push(tejido);
        if (tejido.capturas && tejido.capturas.length > 0) {
          const originalUrl = tejido.capturas[0].image; // URL original
          const imageName = originalUrl.substring(originalUrl.lastIndexOf('/') + 1); // Obtiene el nombre del archivo
          console.log('Imagen seleccionada:', imageName);
          this.imagenSeleccionada = { image: `http://localhost:8011/images/${imageName}` }; // Cambia la URL
        } else {
          console.warn('No se encontraron capturas en el tejido.');
        }
      },
      error: err => {
        console.error('Error al obtener el tejido:', err);
        // Aquí podrías agregar un mensaje para el usuario, si lo deseas
      }
    });
  }

  seleccionarImagen(captura: { image: string }): void {
    // Cambiar la URL de la imagen a la nueva dirección
    const originalUrl = captura.image;
    const imageName = originalUrl.substring(originalUrl.lastIndexOf('/') + 1);
    this.imagenSeleccionada = { image: `http://localhost:8011/images/${imageName}` };
  }

  selectCategory(arg0: string) {
    // Implementa la lógica para seleccionar categorías (notas, sistemas, etc.)
  }
}
