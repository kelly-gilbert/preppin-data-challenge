# -*- coding: utf-8 -*-
"""
Add the challenge title as hover text in the Alteryx tool and Python function
usage tables

Author: Kelly Gilbert
Created: 2022-03-27

Requirements:
- challenge_list.csv (parsed challenge list from Preppin' Data blog)

"""


import pandas as pd


text = """## <a id="alteryx_index"></a>Alteryx Tool Usage &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span title="Return to table of contents"><a href="#contents">⬆️</a></span>

<table>
  <tr>
    <td><b>Category</b></td>
    <td><b>Tool</b></td>
    <td><b>Weeks Used</b></td>
  </tr>

  <tr>
    <td>
      Developer
    </td>
    <td>
      BlockUntilDone
    </td>
    <td>      
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-14/README.md">W14</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-28/README.md">W28</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      DynamicInput
    </td>
    <td>      
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-21/README.md">W21</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-23/README.md">W23</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-25/README.md">W25</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-33/README.md">W33</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-45/README.md">W45</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-46/README.md">W46</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      DynamicRename
    </td>
    <td>      
      <b>2019:</b>&nbsp;&nbsp;
      <a href="2019/preppin-data-2019-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-13/README.md">W13</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-14/README.md">W14</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-20/README.md">W20</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-31/README.md">W31</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-36/README.md">W36</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-39/README.md">W39</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-40/README.md">W40</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-41/README.md">W41</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-43/README.md">W43</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-44/README.md">W44</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      DynamicSelect
    </td>
    <td>      
      <b>2019:</b>&nbsp;&nbsp;
      <a href="2019/preppin-data-2019-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      Field Info
    </td>
    <td>      
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-31/README.md">W31</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      Test
    </td>
    <td>      
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-14/README.md">W14</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-15/README.md">W15</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-18/README.md">W18</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-19/README.md">W19</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-22/README.md">W22</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-46/README.md">W46</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td>
      In/Out
    </td>
    <td>
      textInput
    </td>
    <td>      
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-25/README.md">W25</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-26/README.md">W26</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-29/README.md">W29</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-30/README.md">W30</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td>
      Interface
    </td>
    <td>
      Action
    </td>
    <td>      
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-27/README.md">W27</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      Control Parameter
    </td>
    <td>      
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-20/README.md">W20</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-52/README.md">W52</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      Drop Down
    </td>
    <td>      
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      MacroInput
    </td>
    <td>      
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-20/README.md">W20</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-27/README.md">W27</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-52/README.md">W52</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      MacroOutput
    </td>
    <td>      
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-27/README.md">W27</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-52/README.md">W52</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      Numeric Up Down
    </td>
    <td>      
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-27/README.md">W27</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td>
      Join
    </td>
    <td>
      AppendFields
    </td>
    <td>      
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-18/README.md">W18</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-20/README.md">W20</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-23/README.md">W23</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-27/README.md">W27</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-30/README.md">W30</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-31/README.md">W31</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-33/README.md">W33</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-35/README.md">W35</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-36/README.md">W36</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-41/README.md">W41</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      FindReplace
    </td>
    <td>      
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-22/README.md">W22</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-25/README.md">W25</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-29/README.md">W29</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-34/README.md">W34</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      Join
    </td>
    <td>      
      <b>2019:</b>&nbsp;&nbsp;
      <a href="2019/preppin-data-2019-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-14/README.md">W14</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-15/README.md">W15</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-16/README.md">W16</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-19/README.md">W19</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-20/README.md">W20</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-21/README.md">W21</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-22/README.md">W22</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-23/README.md">W23</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-24/README.md">W24</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-25/README.md">W25</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-26/README.md">W26</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-31/README.md">W31</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-33/README.md">W33</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-34/README.md">W34</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-35/README.md">W35</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-36/README.md">W36</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-38/README.md">W38</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-39/README.md">W39</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-42/README.md">W42</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-43/README.md">W43</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-45/README.md">W45</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-46/README.md">W46</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-47/README.md">W47</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-48/README.md">W48</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-49/README.md">W49</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-51/README.md">W51</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-52/README.md">W52</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-11/README.md">W11</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      JoinMultiple
    </td>
    <td>      
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-17/README.md">W17</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-30/README.md">W30</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-44/README.md">W44</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      Union
    </td>
    <td>      
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-24/README.md">W24</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-25/README.md">W25</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-26/README.md">W26</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-28/README.md">W28</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-33/README.md">W33</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-41/README.md">W41</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-42/README.md">W42</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-43/README.md">W43</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-45/README.md">W45</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-46/README.md">W46</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-52/README.md">W52</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td>
      Macro
    </td>
    <td>
      Batch Macro
    </td>
    <td>      
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-20/README.md">W20</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-52/README.md">W52</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      Iterative Macro
    </td>
    <td>      
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-27/README.md">W27</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td>
      Parse
    </td>
    <td>
      RegEx
    </td>
    <td>      
      <b>2019:</b>&nbsp;&nbsp;
      <a href="2019/preppin-data-2019-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-14/README.md">W14</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-15/README.md">W15</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-17/README.md">W17</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-19/README.md">W19</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-22/README.md">W22</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-29/README.md">W29</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-35/README.md">W35</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-38/README.md">W38</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-39/README.md">W39</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-41/README.md">W41</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-45/README.md">W45</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-52/README.md">W52</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      textToColumns
    </td>
    <td>      
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-15/README.md">W15</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      XMLParse
    </td>
    <td>      
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td>
      Preparation
    </td>
    <td>
      DataCleansing
    </td>
    <td>      
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-23/README.md">W23</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-24/README.md">W24</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      Filter
    </td>
    <td>      
      <b>2019:</b>&nbsp;&nbsp;
      <a href="2019/preppin-data-2019-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-13/README.md">W13</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-14/README.md">W14</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-15/README.md">W15</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-16/README.md">W16</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-17/README.md">W17</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-18/README.md">W18</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-20/README.md">W20</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-21/README.md">W21</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-23/README.md">W23</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-24/README.md">W24</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-25/README.md">W25</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-27/README.md">W27</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-28/README.md">W28</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-31/README.md">W31</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-33/README.md">W33</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-34/README.md">W34</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-35/README.md">W35</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-36/README.md">W36</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-39/README.md">W39</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-40/README.md">W40</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-41/README.md">W41</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-43/README.md">W43</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-44/README.md">W44</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-45/README.md">W45</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-48/README.md">W48</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      Formula
    </td>
    <td>      
      <b>2019:</b>&nbsp;&nbsp;
      <a href="2019/preppin-data-2019-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-13/README.md">W13</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-14/README.md">W14</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-15/README.md">W15</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-16/README.md">W16</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-17/README.md">W17</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-18/README.md">W18</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-19/README.md">W19</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-20/README.md">W20</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-21/README.md">W21</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-23/README.md">W23</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-25/README.md">W25</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-26/README.md">W26</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-27/README.md">W27</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-28/README.md">W28</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-29/README.md">W29</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-30/README.md">W30</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-31/README.md">W31</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-32/README.md">W32</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-33/README.md">W33</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-34/README.md">W34</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-35/README.md">W35</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-36/README.md">W36</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-38/README.md">W38</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-39/README.md">W39</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-40/README.md">W40</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-41/README.md">W41</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-42/README.md">W42</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-43/README.md">W43</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-44/README.md">W44</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-45/README.md">W45</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-46/README.md">W46</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-47/README.md">W47</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-48/README.md">W48</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-49/README.md">W49</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-51/README.md">W51</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-52/README.md">W52</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-11/README.md">W11</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      Formula with Regex
    </td>
    <td>      
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-19/README.md">W19</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-25/README.md">W25</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-29/README.md">W29</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-36/README.md">W36</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-40/README.md">W40</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-51/README.md">W51</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      GenerateRows
    </td>
    <td>      
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-24/README.md">W24</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-26/README.md">W26</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-37/README.md">W37</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-41/README.md">W41</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-42/README.md">W42</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-44/README.md">W44</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      MultiFieldFormula
    </td>
    <td>      
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-18/README.md">W18</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-24/README.md">W24</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-32/README.md">W32</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-33/README.md">W33</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-36/README.md">W36</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-37/README.md">W37</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-40/README.md">W40</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-42/README.md">W42</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-43/README.md">W43</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-44/README.md">W44</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-46/README.md">W46</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-49/README.md">W49</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-51/README.md">W51</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      MultiRowFormula
    </td>
    <td>      
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-13/README.md">W13</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-14/README.md">W14</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-21/README.md">W21</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-25/README.md">W25</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-27/README.md">W27</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-28/README.md">W28</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-30/README.md">W30</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-39/README.md">W39</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-41/README.md">W41</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-42/README.md">W42</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-47/README.md">W47</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-48/README.md">W48</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      RecordID
    </td>
    <td>      
      <b>2019:</b>&nbsp;&nbsp;
      <a href="2019/preppin-data-2019-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-13/README.md">W13</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-15/README.md">W15</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-16/README.md">W16</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-25/README.md">W25</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-30/README.md">W30</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-31/README.md">W31</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-38/README.md">W38</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-51/README.md">W51</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      Sample
    </td>
    <td>      
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-25/README.md">W25</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-29/README.md">W29</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-30/README.md">W30</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-35/README.md">W35</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-36/README.md">W36</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-40/README.md">W40</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-45/README.md">W45</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      Select
    </td>
    <td>      
      <b>2019:</b>&nbsp;&nbsp;
      <a href="2019/preppin-data-2019-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-13/README.md">W13</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-14/README.md">W14</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-16/README.md">W16</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-17/README.md">W17</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-18/README.md">W18</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-20/README.md">W20</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-21/README.md">W21</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-23/README.md">W23</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-27/README.md">W27</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-28/README.md">W28</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-29/README.md">W29</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-31/README.md">W31</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-32/README.md">W32</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-33/README.md">W33</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-35/README.md">W35</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-36/README.md">W36</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-37/README.md">W37</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-38/README.md">W38</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-40/README.md">W40</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-41/README.md">W41</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-42/README.md">W42</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-43/README.md">W43</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-45/README.md">W45</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-46/README.md">W46</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-47/README.md">W47</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-49/README.md">W49</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-51/README.md">W51</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-11/README.md">W11</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      SelectRecords
    </td>
    <td>      
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      Sort
    </td>
    <td>      
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-13/README.md">W13</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-14/README.md">W14</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-16/README.md">W16</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-21/README.md">W21</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-25/README.md">W25</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-27/README.md">W27</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-28/README.md">W28</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-30/README.md">W30</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-36/README.md">W36</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-39/README.md">W39</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-41/README.md">W41</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-42/README.md">W42</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-47/README.md">W47</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-49/README.md">W49</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-51/README.md">W51</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      Tile
    </td>
    <td>      
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      Unique
    </td>
    <td>      
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td>
      Reporting
    </td>
    <td>
      Interactive Chart
    </td>
    <td>      
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      Layout
    </td>
    <td>      
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      Overlay
    </td>
    <td>      
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      Render
    </td>
    <td>      
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      Report text
    </td>
    <td>      
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      Table
    </td>
    <td>      
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td>
      Transform
    </td>
    <td>
      CountRecords
    </td>
    <td>      
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-31/README.md">W31</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      CrossTab
    </td>
    <td>      
      <b>2019:</b>&nbsp;&nbsp;
      <a href="2019/preppin-data-2019-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-15/README.md">W15</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-18/README.md">W18</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-23/README.md">W23</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-31/README.md">W31</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-39/README.md">W39</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-40/README.md">W40</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-43/README.md">W43</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-44/README.md">W44</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      RunningTotal
    </td>
    <td>      
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-37/README.md">W37</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-49/README.md">W49</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      Summarize
    </td>
    <td>      
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-13/README.md">W13</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-14/README.md">W14</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-15/README.md">W15</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-16/README.md">W16</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-17/README.md">W17</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-18/README.md">W18</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-20/README.md">W20</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-21/README.md">W21</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-23/README.md">W23</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-24/README.md">W24</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-25/README.md">W25</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-26/README.md">W26</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-27/README.md">W27</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-28/README.md">W28</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-30/README.md">W30</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-32/README.md">W32</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-33/README.md">W33</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-34/README.md">W34</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-35/README.md">W35</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-36/README.md">W36</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-38/README.md">W38</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-41/README.md">W41</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-42/README.md">W42</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-44/README.md">W44</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-46/README.md">W46</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-47/README.md">W47</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-49/README.md">W49</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-51/README.md">W51</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-52/README.md">W52</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-11/README.md">W11</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      Transpose
    </td>
    <td>      
      <b>2019:</b>&nbsp;&nbsp;
      <a href="2019/preppin-data-2019-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-14/README.md">W14</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-15/README.md">W15</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-16/README.md">W16</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-17/README.md">W17</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-27/README.md">W27</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-28/README.md">W28</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-31/README.md">W31</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-34/README.md">W34</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-36/README.md">W36</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-43/README.md">W43</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-47/README.md">W47</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-48/README.md">W48</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>
</table>
<br>
<br>





## <a id="python_index"></a>Python Function/Method Index &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span title="Return to table of contents"><a href="#contents">⬆️</a></span>

<table>
  <tr>
    <td><b>Category</b></td>
    <td><b>Function/Method/Concept</b></td>
    <td><b>Weeks Used</b></td>
  </tr>

  <tr>
    <td>
      Charts
    </td>
    <td>
      
Bokeh
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

matplotlib
    </td>
    <td>
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-47/README.md">W47</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

Seaborn
    </td>
    <td>
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td>
      Other
    </td>
    <td>

```decimal``` module
    </td>
    <td>
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-11/README.md">W11</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```f strings``` / ```format```
    </td>
    <td>
      <b>2019:</b>&nbsp;&nbsp;
      <a href="2019/preppin-data-2019-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-17/README.md">W17</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-36/README.md">W36</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-41/README.md">W41</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-42/README.md">W42</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-46/README.md">W46</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-51/README.md">W51</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

Function
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-34/README.md">W34</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-35/README.md">W35</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-42/README.md">W42</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-51/README.md">W51</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

Function (recursive)
    </td>
    <td>
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

list methods (```sort```, ```reverse```, ```append```, etc.)
    </td>
    <td>
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-31/README.md">W31</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-34/README.md">W34</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

list/dict comprehension
    </td>
    <td>
      <b>2019:</b>&nbsp;&nbsp;
      <a href="2019/preppin-data-2019-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-11/README.md">W11</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-13/README.md">W13</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-14/README.md">W14</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-16/README.md">W16</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-20/README.md">W20</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-22/README.md">W22</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-24/README.md">W24</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-25/README.md">W25</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-26/README.md">W26</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-27/README.md">W27</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-28/README.md">W28</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-29/README.md">W29</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-30/README.md">W30</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-34/README.md">W34</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-37/README.md">W37</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-38/README.md">W38</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-41/README.md">W41</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-43/README.md">W43</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-45/README.md">W45</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-46/README.md">W46</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-47/README.md">W47</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-48/README.md">W48</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-51/README.md">W51</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

Loops
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-27/README.md">W27</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-33/README.md">W33</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-47/README.md">W47</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-51/README.md">W51</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

Mapping values with dictionary
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-14/README.md">W14</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-29/README.md">W29</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-30/README.md">W30</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-32/README.md">W32</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-34/README.md">W34</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-43/README.md">W43</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-47/README.md">W47</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-48/README.md">W48</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

unpacking a sequence ```*```
    </td>
    <td>
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-41/README.md">W41</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```zip```
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-11/README.md">W11</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-24/README.md">W24</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-37/README.md">W37</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-43/README.md">W43</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td>
      Pandas - Aggregation
    </td>
    <td>

Cumulative aggregation(```cumcount```, ```cumsum```, etc.)
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-49/README.md">W49</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

Named Aggregation
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-17/README.md">W17</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-18/README.md">W18</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-20/README.md">W20</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-22/README.md">W22</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-24/README.md">W24</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-25/README.md">W25</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-26/README.md">W26</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-28/README.md">W28</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-30/README.md">W30</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-32/README.md">W32</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-34/README.md">W34</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-36/README.md">W36</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-38/README.md">W38</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-46/README.md">W46</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-47/README.md">W47</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-49/README.md">W49</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-51/README.md">W51</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```rank```
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-13/README.md">W13</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-14/README.md">W14</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-16/README.md">W16</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-21/README.md">W21</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-25/README.md">W25</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-28/README.md">W28</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-47/README.md">W47</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```groupby``` with filter
    </td>
    <td>
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-23/README.md">W23</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```transform```
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-17/README.md">W17</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-21/README.md">W21</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-33/README.md">W33</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-35/README.md">W35</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-42/README.md">W42</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-49/README.md">W49</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-52/README.md">W52</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-11/README.md">W11</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td>
      Pandas - Dates
    </td>
    <td>

Date Calculations
    </td>
    <td>
      <b>2019:</b>&nbsp;&nbsp;
      <a href="2019/preppin-data-2019-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-18/README.md">W18</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-21/README.md">W21</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-33/README.md">W33</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```DateOffset``` / ```offsets```
    </td>
    <td>
      <b>2019:</b>&nbsp;&nbsp;
      <a href="2019/preppin-data-2019-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-37/README.md">W37</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

Dateparts (```dt.month```, ```dt.quarter```, etc.)
    </td>
    <td>
      <b>2019:</b>&nbsp;&nbsp;
      <a href="2019/preppin-data-2019-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-15/README.md">W15</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-18/README.md">W18</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-29/README.md">W29</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-32/README.md">W32</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-36/README.md">W36</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-42/README.md">W42</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-47/README.md">W47</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-49/README.md">W49</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```date_range```
    </td>
    <td>
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-24/README.md">W24</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-37/README.md">W37</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-42/README.md">W42</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-44/README.md">W44</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```dt.strftime```
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-24/README.md">W24</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-28/README.md">W28</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-49/README.md">W49</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```dt.strptime```
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```read_csv``` with parse_dates
    </td>
    <td>
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-16/README.md">W16</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-26/README.md">W26</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-31/README.md">W31</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-32/README.md">W32</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-39/README.md">W39</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-42/README.md">W42</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-49/README.md">W49</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-51/README.md">W51</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```timedelta``` / ```to_timedelta``` / ```relativedelta```
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-26/README.md">W26</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-33/README.md">W33</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```to_datetime```
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-21/README.md">W21</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-28/README.md">W28</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-29/README.md">W29</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-30/README.md">W30</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-33/README.md">W33</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-45/README.md">W45</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td>
      Pandas - File I/O
    </td>
    <td>

Formatting numeric output
    </td>
    <td>
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-41/README.md">W41</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

Read Excel files
    </td>
    <td>
      <b>2019:</b>&nbsp;&nbsp;
      <a href="2019/preppin-data-2019-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-11/README.md">W11</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-14/README.md">W14</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-15/README.md">W15</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-17/README.md">W17</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-18/README.md">W18</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-19/README.md">W19</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-22/README.md">W22</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-24/README.md">W24</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-25/README.md">W25</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-27/README.md">W27</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-28/README.md">W28</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-29/README.md">W29</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-33/README.md">W33</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-34/README.md">W34</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-35/README.md">W35</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-36/README.md">W36</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-37/README.md">W37</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-38/README.md">W38</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-43/README.md">W43</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-44/README.md">W44</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-45/README.md">W45</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-46/README.md">W46</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-47/README.md">W47</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-48/README.md">W48</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-52/README.md">W52</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

Read Excel files (dynamic sheets)
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-21/README.md">W21</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-23/README.md">W23</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-33/README.md">W33</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-45/README.md">W45</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-46/README.md">W46</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

Write multiple tabs to Excel file
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-14/README.md">W14</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-20/README.md">W20</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-28/README.md">W28</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td>
      Pandas - Joining
    </td>
    <td>

```append```
    </td>
    <td>
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-41/README.md">W41</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```concat```
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-13/README.md">W13</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-25/README.md">W25</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-26/README.md">W26</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-28/README.md">W28</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-33/README.md">W33</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-43/README.md">W43</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-45/README.md">W45</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-46/README.md">W46</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```merge```
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-11/README.md">W11</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-14/README.md">W14</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-15/README.md">W15</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-16/README.md">W16</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-17/README.md">W17</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-18/README.md">W18</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-19/README.md">W19</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-20/README.md">W20</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-22/README.md">W22</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-24/README.md">W24</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-25/README.md">W25</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-26/README.md">W26</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-27/README.md">W27</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-29/README.md">W29</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-34/README.md">W34</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-35/README.md">W35</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-36/README.md">W36</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-38/README.md">W38</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-39/README.md">W39</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-42/README.md">W42</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-45/README.md">W45</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-46/README.md">W46</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-47/README.md">W47</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-52/README.md">W52</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```merge_asof```
    </td>
    <td>
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td>
      Pandas - Other
    </td>
    <td>

```apply``` / ```map```
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-11/README.md">W11</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-16/README.md">W16</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-18/README.md">W18</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-42/README.md">W42</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```assign```
    </td>
    <td>
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-45/README.md">W45</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-46/README.md">W46</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-51/README.md">W51</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-52/README.md">W52</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-11/README.md">W11</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```astype```
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-13/README.md">W13</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-14/README.md">W14</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-15/README.md">W15</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-16/README.md">W16</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-17/README.md">W17</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-19/README.md">W19</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-21/README.md">W21</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-23/README.md">W23</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-25/README.md">W25</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-27/README.md">W27</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-28/README.md">W28</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-30/README.md">W30</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-32/README.md">W32</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-35/README.md">W35</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-44/README.md">W44</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-45/README.md">W45</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-46/README.md">W46</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-48/README.md">W48</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-51/README.md">W51</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```cut``` / ```qcut```
    </td>
    <td>
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-23/README.md">W23</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```factorize```
    </td>
    <td>
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-51/README.md">W51</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```fillna``` / ```ffill``` / ```bfill```
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-13/README.md">W13</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-24/README.md">W24</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-39/README.md">W39</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-42/README.md">W42</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-44/README.md">W44</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-47/README.md">W47</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-48/README.md">W48</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-52/README.md">W52</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-11/README.md">W11</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```reindex```
    </td>
    <td>
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-44/README.md">W44</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```shift``` / ```diff```
    </td>
    <td>
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-30/README.md">W30</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-41/README.md">W41</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```sort_values```
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-13/README.md">W13</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-14/README.md">W14</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-15/README.md">W15</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-25/README.md">W25</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-26/README.md">W26</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-27/README.md">W27</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-30/README.md">W30</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-36/README.md">W36</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-38/README.md">W38</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-39/README.md">W39</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-41/README.md">W41</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-45/README.md">W45</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-51/README.md">W51</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-11/README.md">W11</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td>
      Pandas - Reshaping
    </td>
    <td>

```crosstab```
    </td>
    <td>
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-40/README.md">W40</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```explode```
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-11/README.md">W11</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-15/README.md">W15</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-19/README.md">W19</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-22/README.md">W22</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-24/README.md">W24</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-26/README.md">W26</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-29/README.md">W29</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-37/README.md">W37</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-45/README.md">W45</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-52/README.md">W52</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```extract```
    </td>
    <td>
      <b>2019:</b>&nbsp;&nbsp;
      <a href="2019/preppin-data-2019-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-11/README.md">W11</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-15/README.md">W15</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-17/README.md">W17</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-19/README.md">W19</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-22/README.md">W22</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-25/README.md">W25</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-29/README.md">W29</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-35/README.md">W35</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-38/README.md">W38</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-39/README.md">W39</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-41/README.md">W41</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-48/README.md">W48</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-51/README.md">W51</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```melt```
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-14/README.md">W14</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-15/README.md">W15</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-16/README.md">W16</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-17/README.md">W17</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-27/README.md">W27</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-28/README.md">W28</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-34/README.md">W34</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-36/README.md">W36</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-43/README.md">W43</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-47/README.md">W47</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-48/README.md">W48</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```pivot``` / ```pivot_table```
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-15/README.md">W15</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-18/README.md">W18</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-23/README.md">W23</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-31/README.md">W31</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-39/README.md">W39</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-43/README.md">W43</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-44/README.md">W44</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```stack```
    </td>
    <td>
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

transpose ```T```
    </td>
    <td>
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td>
      Pandas - Selection/slicing
    </td>
    <td>

```drop```
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-14/README.md">W14</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-15/README.md">W15</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-16/README.md">W16</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-17/README.md">W17</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-25/README.md">W25</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-43/README.md">W43</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-45/README.md">W45</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-46/README.md">W46</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-48/README.md">W48</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```drop_duplicates```
    </td>
    <td>
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-25/README.md">W25</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-29/README.md">W29</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-35/README.md">W35</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-45/README.md">W45</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```dropna```
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-15/README.md">W15</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-16/README.md">W16</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-27/README.md">W27</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-48/README.md">W48</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```idmax``` / ```idmin```
    </td>
    <td>
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-24/README.md">W24</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-30/README.md">W30</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-36/README.md">W36</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```query```
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

slicing a DataFrame
    </td>
    <td>
      <b>2019:</b>&nbsp;&nbsp;
      <a href="2019/preppin-data-2019-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-13/README.md">W13</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-14/README.md">W14</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-16/README.md">W16</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-17/README.md">W17</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-19/README.md">W19</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-20/README.md">W20</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-21/README.md">W21</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-22/README.md">W22</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-23/README.md">W23</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-24/README.md">W24</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-25/README.md">W25</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-27/README.md">W27</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-28/README.md">W28</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-29/README.md">W29</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-31/README.md">W31</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-33/README.md">W33</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-34/README.md">W34</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-35/README.md">W35</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-36/README.md">W36</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-39/README.md">W39</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-40/README.md">W40</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-45/README.md">W45</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-48/README.md">W48</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-51/README.md">W51</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-05/README.md">W05</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td>
      Rounding
    </td>
    <td>

Basic
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-11/README.md">W11</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-13/README.md">W13</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-14/README.md">W14</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-20/README.md">W20</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-28/README.md">W28</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-30/README.md">W30</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-32/README.md">W32</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-34/README.md">W34</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-36/README.md">W36</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-38/README.md">W38</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-40/README.md">W40</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-42/README.md">W42</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-49/README.md">W49</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-51/README.md">W51</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

Round Half Up
    </td>
    <td>
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td>
      String Functions
    </td>
    <td>

Changing case (```upper```, ```lower```, ```title```, etc.)
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-19/README.md">W19</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-22/README.md">W22</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-28/README.md">W28</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-29/README.md">W29</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-44/README.md">W44</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-51/README.md">W51</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-52/README.md">W52</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```contains```, ```startswith```, ```endswith```
    </td>
    <td>
      <b>2019:</b>&nbsp;&nbsp;
      <a href="2019/preppin-data-2019-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-22/README.md">W22</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-28/README.md">W28</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-29/README.md">W29</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-48/README.md">W48</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

Count matches
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```findall```
    </td>
    <td>
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-52/README.md">W52</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```join```
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-47/README.md">W47</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-52/README.md">W52</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```ljust``` / ```rjust```
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```match```
    </td>
    <td>
      <b>2019:</b>&nbsp;&nbsp;
      <a href="2019/preppin-data-2019-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```replace```
    </td>
    <td>
      <b>2019:</b>&nbsp;&nbsp;
      <a href="2019/preppin-data-2019-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-02/README.md">W02</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-14/README.md">W14</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-19/README.md">W19</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-27/README.md">W27</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-28/README.md">W28</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-29/README.md">W29</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-34/README.md">W34</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-36/README.md">W36</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-38/README.md">W38</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-48/README.md">W48</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```split```
    </td>
    <td>
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-11/README.md">W11</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-14/README.md">W14</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-15/README.md">W15</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-16/README.md">W16</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-19/README.md">W19</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-21/README.md">W21</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-29/README.md">W29</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-45/README.md">W45</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-06/README.md">W06</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

String slicing
    </td>
    <td>
      <b>2019:</b>&nbsp;&nbsp;
      <a href="2019/preppin-data-2019-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-10/README.md">W10</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-28/README.md">W28</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-33/README.md">W33</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-36/README.md">W36</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```strip```
    </td>
    <td>
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-13/README.md">W13</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-15/README.md">W15</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-16/README.md">W16</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-19/README.md">W19</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-21/README.md">W21</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-22/README.md">W22</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-28/README.md">W28</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-29/README.md">W29</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-43/README.md">W43</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-46/README.md">W46</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-52/README.md">W52</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td>
      numpy
    </td>
    <td>

aggregate functions (e.g. ```sum```, ```max```)
    </td>
    <td>
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```ceil``` / ```floor```
    </td>
    <td>
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-23/README.md">W23</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-47/README.md">W47</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>

  <tr>
    <td></td>
    <td>

```where```
    </td>
    <td>
      <b>2019:</b>&nbsp;&nbsp;
      <a href="2019/preppin-data-2019-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <b>2020:</b>&nbsp;
      <a href="2020/preppin-data-2020-03/README.md">W03</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2020/preppin-data-2020-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
      <b>2021:</b>&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-12/README.md">W12</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-14/README.md">W14</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-15/README.md">W15</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-16/README.md">W16</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-20/README.md">W20</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-28/README.md">W28</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-32/README.md">W32</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-33/README.md">W33</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-34/README.md">W34</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-35/README.md">W35</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-36/README.md">W36</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-39/README.md">W39</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-40/README.md">W40</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-41/README.md">W41</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-42/README.md">W42</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-43/README.md">W43</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-44/README.md">W44</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-47/README.md">W47</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-48/README.md">W48</a>&nbsp;&nbsp;&nbsp;
      <a href="2021/preppin-data-2021-50/README.md">W50</a>&nbsp;&nbsp;&nbsp;
      <b>2022:</b>&nbsp;
      <a href="2022/preppin-data-2022-01/README.md">W01</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-04/README.md">W04</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-07/README.md">W07</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-08/README.md">W08</a>&nbsp;&nbsp;&nbsp;
      <a href="2022/preppin-data-2022-09/README.md">W09</a>&nbsp;&nbsp;&nbsp;
    </td>
  </tr>
</table>
<br>
<br>"""


df_pd = pd.read_csv(r'.\_misc scripts\challenge_list.csv')
df_pd['week'] = df_pd['week'].astype(str)


for i in df_pd.iterrows():
    s = i[1]
    old_text = f'<a href="{s.year}/preppin-data-{s.year}-{s.week.zfill(2)}/README.md">W{s.week.zfill(2)}</a>&nbsp;&nbsp;&nbsp;'
    text = text.replace(old_text,
                        f'<span title="{s.title}">{old_text}</span>')


with open(r'.\misc_scripts\new_html.txt', 'w', encoding='utf-8') as out_file:
        out_file.write(text)
