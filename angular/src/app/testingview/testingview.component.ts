import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

@Component({
  standalone: true,
  imports:[CommonModule],
  selector: 'app-testingview',
  templateUrl: './testingview.component.html',
  styleUrls: ['./testingview.component.css'],
})
export class TestingviewComponent {
  // Placeholders iniciales
  sistemasPlaceholders = [
    { id: 1, nombre: 'Sistema Digestivo' },
    { id: 2, nombre: 'Sistema Nervioso' },
    { id: 3, nombre: 'Sistema Circulatorio' },
  ];

  organosPlaceholders = [
    { id: 1, nombre: 'Estómago' },
    { id: 2, nombre: 'Cerebro' },
    { id: 3, nombre: 'Corazón' },
  ];

  tincionesPlaceholders = [
    { id: 1, nombre: 'H&E' },
    { id: 2, nombre: 'PAS' },
    { id: 3, nombre: 'Tricrómico de Masson' },
  ];

  muestrasPlaceholders = [
    { id: 1, name: 'Muestra 1', sistema: 1, organo: 1, tincion: 1, image: 'https://via.placeholder.com/150' },
    { id: 2, name: 'Muestra 2', sistema: 2, organo: 2, tincion: 2, image: 'https://via.placeholder.com/150' },
    { id: 3, name: 'Muestra 3', sistema: 3, organo: 3, tincion: 3, image: 'https://via.placeholder.com/150' },
  ];

  // Filtros
  selectedFilters: { sistemas: any[]; organos: any[]; tinciones: any[] } = {
    sistemas: [],
    organos: [],
    tinciones: [],
  };

  // Datos filtrados
  filteredSistemas = [...this.sistemasPlaceholders];
  filteredOrganos = [...this.organosPlaceholders];
  filteredTinciones = [...this.tincionesPlaceholders];
  filteredMuestras = [...this.muestrasPlaceholders];

  imagenSeleccionada: any = null;

  // Métodos para filtrar
  filterSistemas(event: any) {
    const query = event.target.value.toLowerCase();
    this.filteredSistemas = this.sistemasPlaceholders.filter((sistema) =>
      sistema.nombre.toLowerCase().includes(query)
    );
  }

  filterOrganos(event: any) {
    const query = event.target.value.toLowerCase();
    this.filteredOrganos = this.organosPlaceholders.filter((organo) =>
      organo.nombre.toLowerCase().includes(query)
    );
  }

  filterTinciones(event: any) {
    const query = event.target.value.toLowerCase();
    this.filteredTinciones = this.tincionesPlaceholders.filter((tincion) =>
      tincion.nombre.toLowerCase().includes(query)
    );
  }

  toggleFilter(item: any, type: 'sistemas' | 'organos' | 'tinciones') {
    const index = this.selectedFilters[type].indexOf(item);
    if (index >= 0) {
      this.selectedFilters[type].splice(index, 1);
    } else {
      this.selectedFilters[type].push(item);
    }
    this.updateMuestras();
  }

  isSelected(item: any, type: 'sistemas' | 'organos' | 'tinciones'): boolean {
    return this.selectedFilters[type].includes(item);
  }

  updateMuestras() {
    this.filteredMuestras = this.muestrasPlaceholders.filter((muestra) => {
      const matchSistema =
        !this.selectedFilters.sistemas.length ||
        this.selectedFilters.sistemas.some((s) => s.id === muestra.sistema);
      const matchOrgano =
        !this.selectedFilters.organos.length ||
        this.selectedFilters.organos.some((o) => o.id === muestra.organo);
      const matchTincion =
        !this.selectedFilters.tinciones.length ||
        this.selectedFilters.tinciones.some((t) => t.id === muestra.tincion);

      return matchSistema && matchOrgano && matchTincion;
    });
  }

  selectCategory(muestra: any) {
    this.imagenSeleccionada = muestra;
  }
}
