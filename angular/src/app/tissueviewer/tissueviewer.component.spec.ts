import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TissueviewerComponent } from './tissueviewer.component';

describe('TissueviewerComponent', () => {
  let component: TissueviewerComponent;
  let fixture: ComponentFixture<TissueviewerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TissueviewerComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TissueviewerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
