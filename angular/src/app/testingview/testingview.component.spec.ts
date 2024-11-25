import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TestingviewComponent } from './testingview.component';

describe('TestingviewComponent', () => {
  let component: TestingviewComponent;
  let fixture: ComponentFixture<TestingviewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TestingviewComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TestingviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
