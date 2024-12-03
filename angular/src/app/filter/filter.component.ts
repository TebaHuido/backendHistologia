import { CommonModule } from '@angular/common';
import { Component, Input, Output, EventEmitter } from '@angular/core';

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
  @Input() allItems: Item[] = [  // Lista completa de elementos que podemos buscar
    { nombre: 'Elemento 1' },
    { nombre: 'Elemento 2' },
    { nombre: 'Elemento 3' },
    { nombre: 'Elemento 4' },
    { nombre: 'Elemento 5' }
  ];
  showDropdown: boolean = false;
  filteredItems: { nombre: string }[] = [];
  selectedItems: { nombre: string }[] = [];
  
  showAllItems() {
    this.filteredItems = [...this.allItems]; // Mostrar todos los elementos
    this.showDropdown = true;
  }
  
  onSearch(event: Event) {
    const searchTerm = (event.target as HTMLInputElement).value.toLowerCase();
    this.filteredItems = this.allItems.filter(item =>
      item.nombre.toLowerCase().includes(searchTerm)
    );
  }
  
  onBlur() {
    setTimeout(() => (this.showDropdown = false), 200); // Cierra el dropdown después de un tiempo
  }
  
  toggleSelection(item: { nombre: string }) {
    const index = this.selectedItems.findIndex(selected => selected.nombre === item.nombre);
    if (index === -1) {
      this.selectedItems.push(item);
    } else {
      this.selectedItems.splice(index, 1);
    }
  }
  
  removeSelection(item: { nombre: string }) {
    this.selectedItems = this.selectedItems.filter(selected => selected.nombre !== item.nombre);
  }
  
  isSelected(item: { nombre: string }): boolean {
    return this.selectedItems.some(selected => selected.nombre === item.nombre);
  }
}  