import { CommonModule } from '@angular/common';
import { Component, Input , Output, EventEmitter} from '@angular/core';

// Definir la interfaz para los elementos que manejaremos
interface Item {
  nombre: string;
}

@Component({
  standalone: true,
  imports: [CommonModule],
  selector: 'app-filter',
  templateUrl: './filter.component.html',
  styleUrls: ['./filter.component.css']
})
export class FilterComponent {
  @Output() filterChange = new EventEmitter<string>();
  filterId: string = 'filter';
  @Input() label: string = 'Elemento';

  // Definimos el tipo 'Item[]' para las variables que almacenan arrays
  filteredItems: Item[] = [];  // Los elementos filtrados
  @Input() allItems: Item[] = [  // Lista completa de elementos que podemos buscar
    { nombre: 'Elemento 1' },
    { nombre: 'Elemento 2' },
    { nombre: 'Elemento 3' },
    { nombre: 'Elemento 4' },
    { nombre: 'Elemento 5' }
  ];
  selectedItems: Item[] = [];  // Elementos seleccionados
  showDropdown = false;  // Controla si mostramos el dropdown de resultados

  // Función para filtrar los elementos basados en la búsqueda
  onSearch(event: any) {
    const searchTerm = event.target.value.toLowerCase();
    this.filteredItems = this.allItems.filter(item => 
      item.nombre.toLowerCase().includes(searchTerm)
    );
    this.showDropdown = this.filteredItems.length > 0;
    this.filterChange.emit(searchTerm); // Emitimos el término de búsqueda
  }

  // Función para manejar la selección de elementos
  toggleSelection(item: Item) {
    if (this.isSelected(item)) {
      // Si el elemento ya está seleccionado, lo eliminamos
      this.selectedItems = this.selectedItems.filter(i => i !== item);
    } else {
      // Si el elemento no está seleccionado, lo agregamos
      this.selectedItems.push(item);
    }
    this.showDropdown = false;  // Ocultamos el dropdown después de la selección
  }

  // Verifica si un elemento está seleccionado
  isSelected(item: Item): boolean {
    return this.selectedItems.includes(item);
  }

  // Se llama cuando el input pierde el foco para cerrar el dropdown
  onBlur() {
    setTimeout(() => {
      this.showDropdown = false;  // Cerramos el dropdown después de perder el foco
    }, 200);  // Retraso para asegurar que el click en el ítem no cierre el dropdown
  }
  removeSelection(item: Item) {
    this.selectedItems = this.selectedItems.filter(i => i !== item);
  }

}
