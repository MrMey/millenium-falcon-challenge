import { Component, ChangeDetectorRef} from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpEventType, HttpHeaders } from '@angular/common/http';
import { DataService } from '../data.service'; // Assurez-vous d'injecter votre service

@Component({
  selector: 'app-file-upload',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './file-upload.html',
  styleUrls: ['./file-upload.scss']
})

export class FileUpload {
  // Propriétés pour l'état de l'upload
  selectedFile: File | null = null;
  uploadProgress: number | null = null;
  uploadSuccess: boolean = false;
  uploadError: string | null = null;
  odds: number | null = null;

  constructor(
    private dataService: DataService, 
    private cdr: ChangeDetectorRef
  ) { }

  // 1. Gère la sélection du fichier
  onFileSelected(event: any): void {
    const file: File = event.target.files[0];

    if (file) {
      this.selectedFile = file;
      this.uploadProgress = null; // Réinitialiser la progression
      this.uploadSuccess = false;
      this.uploadError = null;
    }
  }

  onUpload(): void {
    if (!this.selectedFile) return;

    // 1. Utiliser FileReader pour lire le fichier localement
    const reader = new FileReader();

    reader.onload = (e) => {
      try {
        // Le contenu est une chaîne de caractères (e.target.result)
        const jsonContent = JSON.parse(e.target!.result as string);
        
        // 2. Appeler le service avec l'objet JSON lu
        this.dataService.uploadJsonFile(jsonContent).subscribe({
          next: (response) => {
            console.log('JSON uploadé avec succès !', response.body);
            this.uploadSuccess = true;
            this.uploadError = null;
            this.odds = response.body.odds;

            this.cdr.markForCheck()
          },
          error: (err) => {
            this.uploadError = `Erreur du serveur lors de l'envoi du JSON: ${err.message}`;
            console.error(err);
          }
        });
      
      } catch (error) {
        this.uploadError = "Le fichier sélectionné n'est pas un JSON valide.";
        console.error("Erreur de parsing JSON:", error);
      }
    };

    // 3. Lire le fichier comme une chaîne de caractères (texte)
    reader.readAsText(this.selectedFile);
  }
}