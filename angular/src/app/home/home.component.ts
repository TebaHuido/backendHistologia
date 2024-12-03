import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';
import { Tejido, Categorias } from '../services/tejidos.mock';
import { NgFor, CommonModule } from '@angular/common';
import { FilterComponent } from '../filter/filter.component';

interface Item {
  nombre: string;
}

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
  filteredTejidosItems: { nombre: string }[] = [];
  sistemasUnicosFormateados: { nombre: string }[] = [];

  // Propiedades para diferentes tipos de datos
  categorias: Item[] = [];
  organos: Item[] = [];
  sistemas: Item[] = [];
  tinciones: Item[] = [];
  tags: Item[] = [];

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.api.getTejidos('all').subscribe({
      next: (tejidos: Tejido[]) => {
        this.listaTejidos_all = tejidos;
        this.listaTejidos_show = tejidos;

        // Preparamos los datos
        this.filteredTejidosItems = tejidos.map(te => ({ nombre: te.name })); 
        this.obtenerSistemasUnicos();
      },
      error: err => {
        console.error('Error al obtener todos los tejidos:', err);
      }
    });

    this.api.getFilters().subscribe((data) => {
      this.categorias = this.transformDataToItems(data.categorias);
      this.organos = this.transformDataToItems(data.organos);
      this.sistemas = this.transformDataToItems(data.sistemas);
      this.tinciones = this.transformDataToItems(data.tinciones);
      this.tags = this.transformDataToItems(data.tags);
    });
  }

  private transformDataToItems(data: any[]): Item[] {
    if (!data) return [];
    return data.map((item: any) => ({ nombre: item.name || item }));
  }

  selectCategory(category: string) {
    console.log('Categoría seleccionada:', category);
    if (category === 'all') {
      this.listaTejidos_show = this.listaTejidos_all;
    } else {
      this.api.getTejidos(category).subscribe({
        next: (tejidos: Tejido[]) => {
          this.listaTejidos_show = tejidos;
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
    this.sistemasUnicosFormateados = this.sistemasUnicos.map(sistema => ({ nombre: sistema }));
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
      this.listaTejidos_show = this.listaTejidos_all;
    } else {
      this.listaTejidos_show = this.listaTejidos_all.filter(tejido =>
        tejido.name.toLowerCase().includes(searchTerm)
      );
    }
    this.obtenerSistemasUnicos();
  }
}
