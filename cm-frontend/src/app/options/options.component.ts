import { Component } from '@angular/core';
import { Options } from '../_shared/options';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-options',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './options.component.html',
  styleUrl: './options.component.scss'
})
export class OptionsComponent {
  options: Options = {
    filename: "",
    extension: ".pdf",
    model: "gpt-4o",
    temperature: 0.1,
    context: "default",
    num_nodes: 12,
    show_node_props: false,
    show_edge_props: false,
    show_labels: true
  }

  extensions = [".gif", ".jpeg", ".pdf", ".png", ".svg"]
  models = ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo",
            "mistral-large-latest", "mistral-small-latest", "open-mistral-7b"]
  contexts = ["default", "wiki-text", "scientific", "mathematical"]


  getOptions(): Options {
    return this.options
  }

  resetOptions() {
    this.options = {
      filename: "",
      extension: ".pdf",
      model: "gpt-4o",
      temperature: 0.1,
      context: "default",
      num_nodes: 16,
      show_node_props: false,
      show_edge_props: false,
      show_labels: true
    }
  }
}
