import * as React from 'react';
import './AppContainer.css';

import CustomTextArea from '../CustomTextArea/CustomTextArea';

function AppConainer() {
    const [items, setItems] = React.useState<Item[]>([]);

    return (
        <div className='app-container-style'>
            <CustomTextArea />

            <select name="tags" id="tags">
                <option value="TIPO_DE_RECURSO">Tipo de Recurso</option>
                <option value="ASSUNTO">Assunto</option>
                <option value="FUNDAMENTACAO">Fundamentação</option>
                <option value="RESULTADO_DO_JULGAMENTO">Resultado do Julgamento</option>
            </select>

            <button className='button-style'
                onClick={() => {
                    setItems([...items, getCharacterIndexes()]);
                }}
                onMouseDown={e => {
                    e = e || window.event;
                    e.preventDefault();
                }}>
                Get coordinates
            </button>

            <button className='button-style' onClick={() => downloadItems(items)}>
                Download JSON
            </button>
        </div>
    )
}

function downloadItems(items: Item[]): void {
    const data = {
        'source': (document.getElementById('main-textbox') as HTMLTextAreaElement).value,
        'items': items
    }

    // create file in browser
    const fileName = "items-collection";
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: "application/json" });
    const href = URL.createObjectURL(blob);

    // create "a" HTLM element with href to file
    const link = document.createElement("a");
    link.href = href;
    link.download = fileName + ".json";
    document.body.appendChild(link);
    link.click();

    // clean up "a" element & remove ObjectURL
    document.body.removeChild(link);
    URL.revokeObjectURL(href);
}

function getCharacterIndexes(): Item {
    const txtarea = (document.activeElement as HTMLTextAreaElement);
    const combobox = (document.getElementById('tags') as HTMLSelectElement);

    return {
        'selected-text': txtarea.value.substring(
            txtarea.selectionStart,
            txtarea.selectionEnd
        ),
        'start': txtarea.selectionStart,
        'end': txtarea.selectionEnd,
        'type': combobox.value
    }
}

interface Item {
    'selected-text': String,
    'start': number,
    'end': number,
    'type': String
}

export default AppConainer;
