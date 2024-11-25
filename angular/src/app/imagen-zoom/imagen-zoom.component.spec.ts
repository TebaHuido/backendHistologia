import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImagenZoomComponent } from './imagen-zoom.component';

describe('ImagenZoomComponent', () => {
  let component: ImagenZoomComponent;
  let fixture: ComponentFixture<ImagenZoomComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ImagenZoomComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ImagenZoomComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
