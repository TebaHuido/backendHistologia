import { Component, Input, ChangeDetectorRef, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-imagen-zoom',
  templateUrl: './imagen-zoom.component.html',
  styleUrls: ['./imagen-zoom.component.css'],
  standalone: true,
  imports: [CommonModule],
})
export class ImagenZoomComponent {
  @Input() imageUrl?: string;
  @Input() initialLabels: { x: number; y: number }[] = [];

  scale: number = 1;
  labels: { x: number; y: number }[] = [];
  zoomlimittop: number = 3;
  zoomlimitdown: number = 0.3;
  offsetX: number = 0;
  offsetY: number = 0;
  private isDragging: boolean = false;
  private lastMouseX: number = 0;
  private lastMouseY: number = 0;

  isTaggingMode: boolean = false;
  showLabels: boolean = true;

  @ViewChild('imageContainer', { static: true }) imageContainer!: ElementRef;
  @ViewChild('imageElement', { static: true }) imageElement!: ElementRef;

  constructor(private cdr: ChangeDetectorRef) {}

  ngOnInit(): void {
    this.labels = this.initialLabels?.length ? [...this.initialLabels] : [];
    this.resetZoom();
  }

  resetZoom(): void {
    // Ajustar la imagen al contenedor
    const containerRect = this.imageContainer.nativeElement.getBoundingClientRect();
    const image = new Image();
    image.src = this.imageUrl ?? '';

    image.onload = () => {
      const imageAspectRatio = image.width / image.height;
      const containerAspectRatio = containerRect.width / containerRect.height;

      // Ajustar la imagen para que se ajuste completamente al contenedor al inicio
      if (imageAspectRatio > containerAspectRatio) {
        this.scale = containerRect.width / image.width;
      } else {
        this.scale = containerRect.height / image.height;
      }

      // Centrar la imagen dentro del contenedor
      this.offsetX = (containerRect.width - image.width * this.scale) / 2;
      this.offsetY = (containerRect.height - image.height * this.scale) / 2;

      this.cdr.detectChanges();
    };
  }

  toggleTaggingMode(): void {
    this.isTaggingMode = !this.isTaggingMode;
  }

  toggleLabelsVisibility(): void {
    this.showLabels = !this.showLabels;
  }

  zoomIn(): void {
    if (!this.isTaggingMode && this.scale < this.zoomlimittop) {
      const oldScale = this.scale;
      this.scale += 0.1;
  
      // Centrar el zoom en el centro del contenedor
      const rect = this.imageContainer.nativeElement.getBoundingClientRect();
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      const scaleRatio = this.scale / oldScale;
  
      this.offsetX = centerX - (centerX - this.offsetX) * scaleRatio;
      this.offsetY = centerY - (centerY - this.offsetY) * scaleRatio;
  
      this.limitDrag();
      this.cdr.detectChanges();
    }
  }
  
  zoomOut(): void {
    if (!this.isTaggingMode && this.scale > this.zoomlimitdown) {
      const oldScale = this.scale;
      this.scale -= 0.1;
  
      // Centrar el zoom en el centro del contenedor
      const rect = this.imageContainer.nativeElement.getBoundingClientRect();
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      const scaleRatio = this.scale / oldScale;
  
      this.offsetX = centerX - (centerX - this.offsetX) * scaleRatio;
      this.offsetY = centerY - (centerY - this.offsetY) * scaleRatio;
  
      this.limitDrag();
      this.cdr.detectChanges();
    }
  }
  

  onWheel(event: WheelEvent): void {
    if (this.isTaggingMode) {
      return;
    }
    event.preventDefault();
  
    const zoomIntensity = 0.1;
    const oldScale = this.scale;
  
    // Ajustar la escala directamente sin llamar a zoomIn() o zoomOut()
    if (event.deltaY < 0 && this.scale < this.zoomlimittop) {
      // Zoom In
      this.scale += zoomIntensity;
    } else if (event.deltaY > 0 && this.scale > this.zoomlimitdown) {
      // Zoom Out
      this.scale -= zoomIntensity;
    }
  
    // Calcular el factor de cambio de escala
    const scaleRatio = this.scale / oldScale;
  
    const rect = this.imageContainer.nativeElement.getBoundingClientRect();
    const mouseX = event.clientX - rect.left;
    const mouseY = event.clientY - rect.top;
  
    // Ajustar los offsets para centrar el zoom en el puntero del ratón
    this.offsetX = mouseX - (mouseX - this.offsetX) * scaleRatio;
    this.offsetY = mouseY - (mouseY - this.offsetY) * scaleRatio;
  
    this.limitDrag();
    this.cdr.detectChanges();
  }
  

  onMouseDown(event: MouseEvent): void {
    if (this.isTaggingMode) {
      return;
    }
    event.preventDefault();
    this.isDragging = true;
    this.lastMouseX = event.clientX;
    this.lastMouseY = event.clientY;
  }

  onMouseMove(event: MouseEvent): void {
    if (this.isDragging && !this.isTaggingMode) {
      event.preventDefault();
      const deltaX = event.clientX - this.lastMouseX;
      const deltaY = event.clientY - this.lastMouseY;

      // Invertimos los ejes al arrastrar para que el comportamiento sea el esperado
      this.offsetX -= deltaX;
      this.offsetY -= deltaY;

      this.lastMouseX = event.clientX;
      this.lastMouseY = event.clientY;

      this.limitDrag();
      this.cdr.detectChanges();
    }
  }

  onMouseUp(): void {
    this.isDragging = false;
  }

  onImageClick(event: MouseEvent): void {
    if (!this.isTaggingMode) {
      return;
    }

    const rect = this.imageContainer.nativeElement.getBoundingClientRect();
    const clickX = event.clientX - rect.left;
    const clickY = event.clientY - rect.top;

    const x = (clickX + this.offsetX) / this.scale;
    const y = (clickY + this.offsetY) / this.scale;

    this.labels.push({ x, y });
    this.cdr.detectChanges();
  }

  limitDrag(): void {
    const containerRect = this.imageContainer.nativeElement.getBoundingClientRect();
    const imageWidth = this.imageElement.nativeElement.width * this.scale;
    const imageHeight = this.imageElement.nativeElement.height * this.scale;

    // Limitar el desplazamiento para que no se salga del contenedor
    const minOffsetX = Math.min(0, containerRect.width - imageWidth);
    const minOffsetY = Math.min(0, containerRect.height - imageHeight);
    const maxOffsetX = 0;
    const maxOffsetY = 0;

    // Limitar el desplazamiento dentro de los bordes calculados
    this.offsetX = Math.max(minOffsetX, Math.min(this.offsetX, maxOffsetX));
    this.offsetY = Math.max(minOffsetY, Math.min(this.offsetY, maxOffsetY));

    console.log({
      containerRect,
      imageWidth,
      imageHeight,
      offsetX: this.offsetX,
      offsetY: this.offsetY,
      minOffsetX,
      maxOffsetX,
      minOffsetY,
      maxOffsetY
    });
  }
}
