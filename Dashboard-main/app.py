import base64
import dash
from dash import html, dcc, callback, Input, Output, State
from misc import keypointMappings
from misc.BSL_Backend import *
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import os
import librosa
import plotly.express as px
import pandas as pd
import numpy as np

mp3_files = [file for file in os.listdir('audio/') if file.endswith('.mp3')]


app = dash.Dash(__name__)

app.layout = html.Div([
        html.Div([
            html.H2(['Napier Group Project:'], 
                    style={
                        'font-size':20, 
                        'textAlign':'center',
                        'margin': 0,
                        'font-family': 'Helvetica'
                        }),
            html.H1("BSL in Embodied Music Interaction", 
                    style={
                        'font-size':30, 
                        'textAlign':'center',
                        'margin': 0,
                        'font-family': 'Helvetica'})
        ]),
        
            html.Hr(),

            html.P(['''This project was made as part of the Edinburgh Napier third year group project module (module code) in cooperation with name name, to help aid in reasearch into Embodied music interaction (EMI) with British Sign Language (BSL). 
            This basic analytic web application uses a pure python back end utilizing plotly dash for the graphing and dashing which runs on the flask framework.''']),
            
            html.Div(children=[
                html.H1("Please upload a song and associated openpose file, or start by selecting a song below:"),
                dcc.Upload(id='upload-data',
                        children=html.Div(['Drag and Drop or ',
                            html.A('Select Files')
            ]),style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },multiple=True),
                
            html.Button('Upload', id='upload-button'),
            html.Div(id='output-container'),

            
            html.Hr(style={
                    'margin-top': '20px',
                    'margin-bottom': '20px'}),
        
            html.Label('Select a Song:'),
            #dcc.RadioItems(options=[{'label': 'Apparat Goodbye', 'value': 'Apparat_Goodbye'},
             #                       {'label': 'DaftPunk', 'value': 'daft'}], 
              #                      id='song-selector', persistence="session"),
                dcc.RadioItems(options=[{'label': file, 'value': file} for file in mp3_files], 
                                  id='song-selector', persistence="session"),
                
            html.Hr(style={
                    'margin-top': '20px',
                    'margin-bottom': '20px'}),
                    
            html.Label('Select which participant:'),
            dcc.RadioItems(options=[{'label': 'One', 'value': 'P1'},
                                    {'label': 'Two', 'value': 'P2'},
                                    {'label': 'Three', 'value': 'P3'}], id='participant-selector'),
        
            html.Hr(style={
                    'margin-top': '20px',
                    'margin-bottom': '20px'}),
        
            html.Label('Isolate particular body parts?'),
            dcc.RadioItems(options=[{'label':'Yes', 'value':'display'},
                                    {'label':'No', 'value':'doNotDisplay'}], value='doNotDisplay', id='toggleHideSelection'),
        
            html.Div([
                html.Div([html.Label('Body Keypoints'),
                    dcc.RadioItems(options=[{'label': 'Yes', 'value': 'yes'},
                                            {'label': 'No', 'value': 'no'}],
                                            value='no', 
                                            style={
                                            'display': 'flex', 
                                            'flex-direction': 'column'},
                                            id='radioBody')]),
                    
                html.Div([html.Label('Face Keypoints'),
                    dcc.RadioItems(options=[{'label': 'Yes', 'value': 'yes'},
                                            {'label': 'No', 'value': 'no'}],
                                            value='no', 
                                            style={
                                            'display': 'flex', 
                                            'flex-direction': 'column'},
                                            id='radioFace')]),
                    
                html.Div([html.Label('Hand Keypoints'),
                    dcc.RadioItems(options=[{'label': 'Yes', 'value': 'yes'},
                                            {'label': 'No', 'value': 'no'}],
                                            value='no', 
                                            style={
                                            'display': 'flex', 
                                            'flex-direction': 'column'},
                                            id='radioHand')])
                ],style={
                'display': 'flex',
                'justify-content': 'space-between',
                'margin-top': '20px',
                'margin-bottom': '20px'}, 
                id='elementToHide'),
            
            html.Hr(style={
                    'margin-top': '20px',
                    'margin-bottom': '20px'}),
            
            html.Div([
                dcc.Checklist(options=[{'label': keypoint, 'value': keypoint} for keypoint in keypointMappings.bodyMappings.values()],
                              style={
                              'display': 'flex',
                              'justify-content': 'space-between',
                              'flex-direction': 'row',
                              'padding': '10px'
                              }, id='bodyKeypoints')],style={
                                  'margin-top': '20px',
                                  'margin-bottom': '20px'}),
                
            html.Div([
                dcc.Checklist(options=[{'label': keypoint, 'value': keypoint} for keypoint in keypointMappings.faceMappings.values()],
                              style={
                              'display': 'flex',
                              'justify-content': 'space-between',
                              'flex-wrap': 'wrap',
                              'flex-direction': 'row',
                              'padding': '10px'
                              })],style={
                                  'margin-top': '20px',
                                  'margin-bottom': '20px'}, 
                              id='faceKeypoints'),   
            
            html.Div([
                dcc.Checklist(options=[{'label': keypoint, 'value': keypoint} for keypoint in keypointMappings.hand_mappings.values()],
                              style={
                              'display': 'flex',
                              'justify-content': 'space-between',
                              'flex-direction': 'row',
                              'padding': '10px'
                              })],style={
                                  'margin-top': '20px',
                                  'margin-bottom': '20px'}, 
                              id='handKeypoints'),           
                ], 
                style={
                'padding': 10, 
                'flex': 1, 
                'background-color': '#D3D3D350'}),
            
            dcc.Graph(id='scatter-plot', style={'height': '70vh', 'width': '100vw', 'max-height': '1080px', 'max-width': '1920px'}),
            dcc.Graph(id='waveform'),
            dcc.Graph(id='deltas'),
            dcc.Loading(dcc.Graph(id="animation"), type="cube")


], style={
    'display': 'flex', 
    'flex-direction': 'column', 
    'margin-left':'250px',
    'margin-right':'250px'})
            
#####################
### Callback Time ###
#####################

## First 
@app.callback(
    Output('elementToHide','style'),
    Input('toggleHideSelection','value'))
def show_hide_keypoint_group(value):
    if value == 'display':
        return  {'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between', 'margin-top': '20px', 'margin-bottom': '20px'}
    if value == 'doNotDisplay':
        return {'display': 'none', 'flex': '1'}

## Second
@app.callback(
    Output('bodyKeypoints','style'),
    Input('radioBody','value'))
def show_hide_body_options(value):
    if value == 'yes':
        return {'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between', 'margin-top': '20px', 'margin-bottom': '20px'}
    if value == 'no':
        return {'display': 'none', 'flex': '1'}
    
## Third
@app.callback(
    Output('faceKeypoints','style'),
    Input('radioFace','value'))
def show_hide_face_options(value):
    if value == 'yes':
        return {'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between', 'margin-top': '20px', 'margin-bottom': '20px'}
    if value == 'no':
        return {'display': 'none', 'flex': '1'}
    
## Fourth
@app.callback(
    Output('handKeypoints','style'),
    Input('radioHand','value'))
def show_hide_face_options(value):
    if value == 'yes':
        return {'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between', 'margin-top': '20px', 'margin-bottom': '20px'}
    if value == 'no':
        return {'display': 'none', 'flex': '1'}

## Graph Callback
@app.callback(
    Output('scatter-plot','figure'),
    Input('bodyKeypoints', 'value'),
    Input('song-selector', 'value'),
    Input('participant-selector', 'value'))
def update_graph(value1, value2, value3):
    traces = []
    fileName = 'data/' + value2[:-4] + '_' + value3 + '_features' + '.json'
    for keypoint in value1:
        data = ConvertData(fileName)
        x = data['body'][keypoint][0]
        y = data['body'][keypoint][1]
        traces.append(go.Scatter(x=x, y=1080-y, mode='markers', name=keypoint, marker=dict(opacity=0.5)))
        layout = go.Layout(
            title='Scatter Plot with Checklists',
            xaxis=dict(title='X-axis', range=[0, 1920]),
            yaxis=dict(title='Y-axis', range=[0, 1080]),
        )
    return {'data': traces, 'layout': layout}


    
@app.callback(Output('output-container', 'children'),
              Input('upload-button', 'n_clicks'),
              State('upload-data', 'filename'),
              State('upload-data', 'contents'))
def save_uploaded_files(n_clicks, filenames, contents):
    if n_clicks:
        for filename, content in zip(filenames, contents):
            decoded_content = base64.b64decode(content)
            if filename.endswith('.mp3'):
                folder = 'audio'
            elif filename.endswith('.json'):
                folder = 'data'
            else:
                folder = 'other_files'
            with open(os.path.join(folder, filename), 'wb') as f:
                f.write(decoded_content)
        return html.Div([
            html.P(f"File {filename} uploaded successfully") for filename in filenames
        ])
        
# Wave form

@app.callback(
    Output('waveform', 'figure'),
    Input('song-selector', 'value'))
def makeWaveFormGraph(value):
     if value == value:
        y, sr = librosa.load('audio/' + value)
        stft = librosa.stft(y)
        spectrogram = librosa.amplitude_to_db(np.abs(stft))
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=np.arange(len(y))/sr, y=y))
        fig.update_layout(title='Audio Clip Waveform Visualization',
               xaxis_title='Time (s)',
               yaxis_title='Amplitude')
        return fig    
    
    #deltas call back
@app.callback(
    Output('deltas', 'figure'),
    Input('bodyKeypoints', 'value'),
    Input('song-selector', 'value'),
    Input('participant-selector', 'value'))
def deltas(value1, value2, value3):
    traces = []
    fileName = 'data/' + value2[:-4] + '_' + value3 + '_features' + '.json'
    data = ConvertData(fileName)
    for keypoint in value1:
        x = []
        x.append(keypoint)
        y = []
        y.append(sum(abs(getDeltaFromPositions(data['body'][keypoint])[1])))
        traces.append(go.Bar(x=x, y=y, name=keypoint))
        layout = go.Layout(
            title='Scatter Plot with Checklists')
    return {'data': traces, 'layout': layout}

@app.callback(
    Output('animation', 'figure'),
    Input('song-selector', 'value'),
    Input('participant-selector', 'value'))
def animation(value1, value2):
    fileName = 'data/' + value1[:-4] + '_' + value2 + '_features' + '.json'
    data = ConvertData(fileName)
    aniList = getAnimation(data)
    aniListSp = aniList["body"] + aniList["face"] + aniList["hand_left"] + aniList['hand_right']
    aniNP = np.array(aniListSp)
    df = pd.DataFrame(aniNP, columns=['x', 'y', 'frame'])
    print(df.head())
    animation = px.scatter(df, x="x", y="y", animation_frame="frame", range_x=[0,1920], range_y=[0,1080], title="Animation", width=960, height=540)

    return animation


if __name__ == '__main__':
    app.run_server(port=8051, debug=False)