import { TestBed } from '@angular/core/testing';

import { TejidosService } from './tejidos.service';

describe('TejidosService', () => {
  let service: TejidosService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TejidosService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
