from importlib import import_module

from horde.classes.base import Suspicions

from .. import args

main_class = import_module(name=f"horde.classes.{args.horde}")

# Should figure out an elegant way to do this with a for loop
WaitingPrompt = main_class.WaitingPrompt
ProcessingGeneration = main_class.ProcessingGeneration
Worker = main_class.Worker
PromptsIndex = main_class.PromptsIndex
GenerationsIndex = main_class.GenerationsIndex
User = main_class.User
Team = main_class.Team
Database = main_class.Database
News = main_class.News


# from .base import WaitingPrompt,ProcessingGeneration,Worker,PromptsIndex,GenerationsIndex,User,Database

db = Database(convert_flag=args.convert_flag)
waiting_prompts = PromptsIndex()
processing_generations = GenerationsIndex()
