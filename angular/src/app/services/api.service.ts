import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Categorias, Tejido, Muestra } from '../services/tejidos.mock';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  getCategorias(): Observable<Categorias[]> {
    return this.http.get<Categorias[]>(`${this.apiUrl}/categorias`);
  }

  getTejidos(category: string): Observable<Tejido[]> {
    return this.http.get<Tejido[]>(`${this.apiUrl}/muestras/por_categoria/?category=${category}`);
  }

  getTejido(id: number): Observable<Muestra> {
    return this.http.get<Muestra>(`${this.apiUrl}/muestra3/${id}`);
  }
}
