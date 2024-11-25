import { Injectable } from '@angular/core';
import { ITejido, tejidosArray } from './tejidos.mock';

@Injectable({
  providedIn: 'root'
})
export class TejidosService {

  constructor() { }

  getTejidos(): ITejido[] {
    return tejidosArray;
  }
}
