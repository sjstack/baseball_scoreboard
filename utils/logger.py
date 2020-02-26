
import os
import traceback

from datetime import datetime

def log( text, tag = None, timestamp = False ):
    if "log_of" not in globals():
        global log_of

        log_dir = os.path.dirname( os.path.realpath(__file__) ) + "/../log/"
        if not os.path.exists( log_dir ):
            os.makedirs( log_dir )
        
        log_fname = log_dir + "scoreboard_emulator.log"
        log_of = open( log_fname, 'w+' )

    log_entry = (str(datetime.now()) if timestamp else "") + ((" ["+tag+"] ") if None != tag else "")
    log_entry += f"{text}\n"

    log_of.write( log_entry )
    log_of.flush()

def log_exception( exception ):    
    log( exception, "Exception", True )
    stack_trace = traceback.format_exc()
    log( stack_trace )
    
def log_error( error ):
    log( error, "Error", True )

def log_warning( warning ):
    log( warning, "Warning", True )

def log_status( status ):
    log( status, "Status", True )


