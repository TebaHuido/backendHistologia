import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Tejido } from './tejidos.mock';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  getTejidos(category: string): Observable<Tejido[]> {
    return this.http.get<Tejido[]>(`${this.baseUrl}/tejidos`, { params: { category } });
  }

  getTejido(id: number): Observable<Tejido> {
    return this.http.get<Tejido>(`${this.baseUrl}/tejidos/${id}`);
  }

  getFilters(): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/filters`);
  }

  filterMuestras(filters: any): Observable<Tejido[]> {
    let params = new HttpParams();
    Object.keys(filters).forEach(key => {
      filters[key].forEach((value: string) => {
        params = params.append(key, value);
      });
    });
    return this.http.get<Tejido[]>(`${this.baseUrl}/muestras/filtrado/`, { params });
  }

  addNota(nota: any): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/notas/`, nota);
  }
}