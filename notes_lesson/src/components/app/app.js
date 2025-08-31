import {Component} from 'react';

import NoteAddForm from '../note-add-form/note-add-form';
import NoteList from '../note-list/note-list';
import SearchPanel from '../search-panel/search-panel';
import AppFilter from '../app-filter/app-filter';
import NoteInfo from '../note-info/note-info';

import './app.css';

class App  extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: [ 
                {title:"Note 1",important:true,id:1,date:'21.02.2022',text:"Contrary to popular belief, Lorem Ipsum is not simply random text."},
                {title:"Note 2",important:false,id:2,date:'07.09.2022',text:"The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested."},
                {title:"Note 3",important:false,id:3,date:'15.12.2022',text:"Sections 1.10.32 and 1.10.33 from end"}
            ],
            term:'',
            filter: 'all'
        }
        this.maxId = 4
    }

    deleteItem = (id) => {
       this.setState(({data}) => {
        return {
            data:data.filter(item => item.id !== id)
        }
       })
    }

    addItem = (title,text) => {
        const current = new Date();
        const date = (current.getDate()<10?'0'+current.getDate():current.getDate())+'.'+(current.getMonth()+1<10?'0'+(current.getMonth()+1):current.getMonth()+1)+'.'+current.getFullYear();
        const newItem = {title,text,important:false,date,id:this.maxId++};
        this.setState(({data}) => {
            const newArr = [...data,newItem];
            return {
                data:newArr
            }
        })
    }

    onToggleImportant = (id) => {
        this.setState(({data}) => ({
            data:data.map(item => {
                if(item.id === id) {
                    return {...item,important: !item.important}
                } return item;
            })
        }))
    }

    searchNote = (items,term) => {
        if(term.length === 0) {
            return items;
        } return items.filter(item => {
            return item.text.indexOf(term) > -1
        })
    }

    onUpdateSearch = (term) => {
        this.setState({term});
    }

    filterPost = (items,filter) => {
        switch(filter) {
            case 'important': return items.filter(item => item.important);
        default: return items
        }
    }

    onFilterSelect = (filter) => {
        this.setState({filter});
    }

    render() {
        const {data,term,filter} = this.state;
        const notes = data.length;
        const importanted = data.filter(item => item.important).length;
        const visibleData = this.filterPost(this.searchNote(data,term),filter);

        return (
            <div className="app">
                <NoteInfo
                    notes={notes}
                    importanted={importanted}/>
                <div className="search-panel">
                    <SearchPanel
                        onUpdateSearch={this.onUpdateSearch}/>    
                </div>
                    <AppFilter
                       filter={filter}
                       onFilterSelect={this.onFilterSelect} />  
                    <NoteAddForm
                        onAdd={this.addItem}/>
                    <NoteList 
                        data={visibleData}
                        onDelete={this.deleteItem}
                        onToggleImportant={this.onToggleImportant}/>
                    
            </div>
        )
    }   
}

export default App;