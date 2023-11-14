# PPE_Detecting_Prototype

## INSTALLATION
Global Requirements for the system:
    - Git
    - Python
    - pip
    - virtualenv (optional)
STEPS
Step 1 -  Go to Github Repository: https://github.com/2020251-CPE/PPE_Detecting_Prototype
Step 2 - Clone Repository to desired location. ( Make sure you have git installed in your system )
    > git clone https://github.com/2020251-CPE/PPE_Detecting_Prototype.git
Step 3 - Go to project directory and install packages according to the requirements.txt 
         using 'pip install -r requirements.txt'
    Note: It is best practice to separate packages from the global system to avoid 
    dependencies conflict with other projects. To do this, create a virtual environment 
    first instead of directly doing 'pip install' 
    > pyhton -m venv <virtualenv-name>
    Then, activate the virtual environmentwith te following Code:
    (in Windows CMD)        > virtualenv-name/Scripts/activate.bat
    (in Windows Powershell) > virtualenv-name/Scripts/activate.ps1
    (in Linux Terminal)     > source /virtualenv-name/bin/activate
    Lastly, install packages to vertual environment
    > pip install -r requirements.txt
    You'll know the packages installed in the Virtual environment when the packages
    are found in the lib/ directory of the VirtualEenvironment folder
Step 4 - Proceed to Application Execution Part of the Documentation to ruun the program 

## APPLICATION EXECUTION
Step 1 - To Start the app and execute the program, the user must first complete the 'INSTALLATION' portion of the page.
Step 2 - If said task is fully completed, run Flask by using the following command in your Terminal/CMD:
    > python app.py
    A prompt will appear, among other things, that shows the localhost locations as well as a port where the OptiSafe is available. such prompts usually appear as such:
    > localhost:5000 or 127.0.0.1:5000
Step 3 - Finally, Ctrl + Click that localhost address or type said address to a Browser's Web address to finally run the WebApp
Step 4 - bring or wear a PPE to Test it in front of your Webcam/camera
NOTE: As of Writing the following are PPEs that the app's Model is trained for and therefore, may detect more in production:
- Apron 
- Bunny Suit
- Gloves
- Respiratory Mask
- Head Cap
- Goggles