import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';
import { Tejido, Categorias } from '../services/tejidos.mock';
import { NgFor, CommonModule } from '@angular/common';
import { FilterComponent } from '../filter/filter.component';
@Component({
  selector: 'app-home',
  standalone: true,
  imports: [NgFor, CommonModule, FilterComponent],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  listaTejidos_all: Tejido[] = [];
  listaTejidos_show: Tejido[] = [];
  listaCategorias: Categorias[] = [];
  sistemasUnicos: string[] = [];
  filteredTagsItems: { nombre: string }[] = [];
  constructor(private api: ApiService) {}
  filteredTejidosItems: { nombre: string }[] = [];
  sistemasUnicosFormateados: { nombre: string }[] = [];
  ngOnInit(): void {
    this.api.getTejidos('all').subscribe({
      next: (tejidos: Tejido[]) => {
        this.listaTejidos_all = tejidos;
        this.listaTejidos_show = tejidos;
        this.filteredTejidosItems = tejidos.map(te => ({ nombre: te.name })); // Preparamos los datos
        this.obtenerSistemasUnicos();
      },
      error: err => {
        console.error('Error al obtener todos los tejidos:', err);
      }
    });
  }

  selectCategory(category: string) {
    console.log('Categoría seleccionada:', category);
    if (category === 'all') {
      this.listaTejidos_show = this.listaTejidos_all;
    } else {
      this.api.getTejidos(category).subscribe({
        next: (tejidos: Tejido[]) => {
          this.listaTejidos_show = tejidos;
          console.log('Tejidos filtrados:', this.listaTejidos_show);
          this.obtenerSistemasUnicos();
        },
        error: err => {
          console.error('Error al obtener tejidos por categoría:', err);
        }
      });
    }
    this.obtenerSistemasUnicos();
  }

  obtenerSistemasUnicos() {
    const sistemasSet = new Set<string>();
    this.listaTejidos_show.forEach(tejido => {
      if (tejido.sistema) {
        sistemasSet.add(tejido.sistema);
      }
    });
    this.sistemasUnicos = Array.from(sistemasSet);
    console.log('Sistemas únicos:', this.sistemasUnicos);
  
    // Formatear los sistemas únicos después de actualizarlos
    this.sistemasUnicosFormateados = this.sistemasUnicos.map(sistema => ({ nombre: sistema }));
    console.log('Sistemas únicos formateados:', this.sistemasUnicosFormateados);
  }

  drawPoint(event: MouseEvent) {
    console.log(event.offsetX, event.offsetY);
  }

  getMuestrasPorSistema(sistema: string): Tejido[] {
    return this.listaTejidos_show.filter(muestra => muestra.sistema === sistema);
  }

  getMuestrasSinSistema(): Tejido[] {
    return this.listaTejidos_show.filter(muestra => !muestra.sistema);
  }
  filterMuestras(searchTerm: string) {
    if (!searchTerm) {
      this.listaTejidos_show = this.listaTejidos_all; // Restaurar lista completa
    } else {
      this.listaTejidos_show = this.listaTejidos_all.filter(tejido =>
        tejido.name.toLowerCase().includes(searchTerm)
      );
    }
    this.obtenerSistemasUnicos(); // Actualizar los sistemas únicos
  }
}
