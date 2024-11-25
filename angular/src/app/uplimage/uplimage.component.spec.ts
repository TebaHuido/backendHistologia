import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UplimageComponent } from './uplimage.component';

describe('UplimageComponent', () => {
  let component: UplimageComponent;
  let fixture: ComponentFixture<UplimageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UplimageComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(UplimageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
