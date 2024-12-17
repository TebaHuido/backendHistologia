import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Tejido, Muestra } from './tejidos.mock';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:8000/api'; // Cambia esto a tu URL de backend

  constructor(private http: HttpClient) {}

  getTejidos(category: string, headers: HttpHeaders): Observable<Tejido[]> {
    return this.http.get<Tejido[]>(`${this.baseUrl}/tejidos/?category=${category}`, { headers });
  }

  getFilters(headers: HttpHeaders): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/filters/`, { headers });
  }

  filterMuestras(filters: any, headers: HttpHeaders): Observable<Tejido[]> {
    return this.http.post<Tejido[]>(`${this.baseUrl}/filter-muestras/`, filters, { headers });
  }

  getTejido(id: number, headers: HttpHeaders): Observable<Tejido> {
    return this.http.get<Tejido>(`${this.baseUrl}/tejidos/${id}/`, { headers });
  }

  addNota(nota: any, headers: HttpHeaders, options: any): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/notas/`, nota, { headers, ...options });
  }

  updateNota(id: number, nota: any, headers: HttpHeaders): Observable<any> {
    return this.http.put<any>(`${this.baseUrl}/notas/${id}/`, nota, { headers });
  }

  updateSample(id: number, sample: any, headers: HttpHeaders): Observable<any> {
    return this.http.put<any>(`${this.baseUrl}/samples/${id}/`, sample, { headers });
  }
}