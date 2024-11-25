import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NotesComponent } from './notes.component';
//rJyCTPO03OikwN4xc9ViIaAJWX7H/d5PTsAZAZJ0N9Om3TIBgO8ijXlrhmodc0MhKtZVPE/MZv8fz0UYVIaBkwTjpDxu8XMHXb/pYta6R+plb1JzV55vYf3RhfWuC375Zd0VUqlg6N+9vInMX+2ym0zQ7ZDim8pzSAqEP+MzNYfLMAnU86Za0DPadTecvKZU
describe('NotesComponent', () => {
  let component: NotesComponent;
  let fixture: ComponentFixture<NotesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NotesComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(NotesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
