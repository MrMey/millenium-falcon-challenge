import { Component, ChangeDetectorRef} from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpEventType, HttpHeaders } from '@angular/common/http';
import { DataService } from '../data.service';

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
  status: string = "Will the falcon reach the planet in time?";

  constructor(
    private dataService: DataService, 
    private cdr: ChangeDetectorRef
  ) { }

  onFileSelected(event: any): void {
    const file: File = event.target.files[0];

    if (file) {
      this.selectedFile = file;
      this.uploadProgress = null;
      this.uploadSuccess = false;
      this.uploadError = null;
    }
  }

  onUpload(): void {
    if (!this.selectedFile) return;

    const reader = new FileReader();

    reader.onload = (e) => {
      try {
        const jsonContent = JSON.parse(e.target!.result as string);
        
        this.dataService.uploadJsonFile(jsonContent).subscribe({
          next: (response) => {
            console.log('JSON uploadé avec succès !', response.body);
            this.uploadSuccess = true;
            this.uploadError = null;
            this.odds = response.body.odds;
            
            if (this.odds === 100) {
              this.status = "Congrats! The falcon has reached the planet in time!";
            } else if (this.odds == 0) {
              this.status = "Damned the Falcon hasn't reached the planet in time";
            }
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

    reader.readAsText(this.selectedFile);
  }
}