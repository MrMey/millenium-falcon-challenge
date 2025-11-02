import { Injectable } from '@angular/core';
import { HttpClient, HttpEvent, HttpEventType, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  // Remplacez par l'URL de votre endpoint d'upload (côté serveur)
  private uploadUrl = 'http://localhost:5000/router'; 

  constructor(private http: HttpClient) { }

  /**
   * Envoie le fichier au serveur en utilisant FormData.
   * @param file Le fichier à uploader.
   * @returns Un Observable qui émet des événements de progression et de réponse.
   */
uploadJsonFile(jsonContent: any): Observable<any> {
    // 1. Définition des en-têtes avec Content-Type: application/json
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json' 
      }),
      // On peut laisser 'reportProgress: false' car il n'y a pas de gros flux de données
      observe: 'response' as const // Observez la réponse complète pour le statut
    };

    // 2. Exécution de la requête POST: Angular sérialise automatiquement jsonContent en JSON.
    return this.http.post(
      this.uploadUrl, 
      jsonContent, // <-- Le contenu JSON est envoyé ici
      httpOptions
    );
  }
}