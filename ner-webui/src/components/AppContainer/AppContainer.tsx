import * as React from 'react';
import './AppContainer.css';

import CustomTextArea from '../CustomTextArea/CustomTextArea';

function AppConainer() {
    const [items, setItems] = React.useState<Item[]>([]);

    return (
        <div className='row-container-style'>
            <div className='column-container-style' style={{'flex': 2}}>
                <CustomTextArea />

                <select name="tags" id="tags">
                    <option value="TYPE_OF_APPEAL">Type of Appeal - Request for Standardization</option>
                    <option value="SUBJECT">Subject</option>
                    <option value="RATIO_DECIDENDI">Ratio Decidendi</option>
                    
                    <option value="NOT_HEARD">Not Heard RS by TNU</option>
                    <option value="SUSPENDED">Suspended RS by TNU</option>
                    <option value="NOT_ENTERTAINED">Not Entertained RS by TNU</option>
                    <option value="GRANTED_TO_REVOKE">RS Granted to Revoke Decision by TNU</option>
                    <option value="NOT_GRANTED">Not Granted RS by TNU</option>
                    <option value="GRANTED">Granted RS by TNU</option>
                    <option value="GRANTED_AND_INDICATED">RS Granted and Indicated to Affect Theme by TNU</option>
                </select>

                <div className='row-container-style' style={{'height': 'unset', 'gap': '20px'}}>
                    <button className='button-style'
                        onClick={() => {
                            const newItem = getCharacterIndexes()
                            if (newItem != null)
                                setItems([...items, newItem]);
                        }}
                        onMouseDown={e => {
                            e = e || window.event;
                            e.preventDefault();
                        }}>
                        Tag Item
                    </button>

                    <button className='button-style'
                        onClick={() => {
                            setItems([]);
                        }}>
                        Clear Item List
                    </button>
                </div>

                <button className='button-style' onClick={() => downloadItems(items)}>
                    Download JSON
                </button>
            </div>

            <div className='column-container-style' style={{'flex': 1}}>
                <p>Extracted Items</p>

                <ul id='items-collection' className='items-collection'>
                    { 
                        items.map(item => {
                            return (
                                <li style={{'margin': '30px 0'}}>
                                    <div style={{'display': 'flex', 'flexDirection': 'column'}}>
                                        { item['selected-text'] } - { item['type'] } - { item['start'] }..{ item['end'] }
                                    </div>
                                </li>
                            );
                        })
                    }
                </ul>
            </div>
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

function getCharacterIndexes(): Item | null {
    const txtarea = (document.activeElement as HTMLTextAreaElement);
    const combobox = (document.getElementById('tags') as HTMLSelectElement);

    if (txtarea.value == "" || txtarea.selectionStart == txtarea.selectionEnd) {
        return null;
    }

    console.log('not null');

    console.log(txtarea.value);
    console.log(txtarea.selectionStart);
    console.log(txtarea.selectionEnd);    
    
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
