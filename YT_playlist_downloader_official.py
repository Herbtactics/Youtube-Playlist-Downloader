from pytube import YouTube, Playlist
import sys, os
from concurrent.futures import ThreadPoolExecutor

print(r'Input the folder location which you want to download the video to; Ex: C:\Users\Herbtactics\Desktop\New folder\music folder init test\ ') # the r turns the str into a raw str, which allows for '\'
music_input = input('\n>>>')
music_location = music_input
music_location.encode('unicode_escape') # this turns '\' into '\\' so it can be interpreted by python

# test playlist - https://www.youtube.com/playlist?list=PLQj9uaa83-3jhKMHFtADbP67R26B3GSjw

loop_1 = True
while loop_1 == True:
    try:
        playlist_link = input('Playlist URL:')
        print('\ncompiling list...\n')
        video_links = Playlist(playlist_link).video_urls

        def downloading_process(x):
            try:
                yt = YouTube(x)
                video = yt.streams.filter(only_audio=True).first() # first() is to take the first result given from the url / reference line for Key Error(age restriction) exception handling
                dwnld_file = video.download(music_location)
                new_file, ext = os.path.splitext(dwnld_file)
                os.rename(dwnld_file, new_file + '.mp3')
                name_of_file = new_file.replace(music_location,'')
                print('\n', name_of_file, 'has been downloaded')

            except FileExistsError: # if the user tries to download a video that has already been downloaded
                position = url_list.index(x)
                print('\n', titles_readable[position], 'ALREADY EXISTS')
                if os.path.exists(new_file + '.mp4'): 
                    os.remove(new_file + '.mp4') # removes the .mp4 download of the duplicate video
            except KeyError: # for videos that have been age-restricted
                exc_type, exc_obj, exc_tb = sys.exc_info() # exc-tb is needed to tell the program what line the exception occured on(need the other 2 exc in order for sys.exc to function)
                if exc_tb.tb_lineno == 22:
                    position = url_list.index(x)
                    print('\n', titles_readable[position], 'IS AGE RESTRICTED CANNOT DOWNLOAD')
            # we put certain exceptions in the def in order to continue with the next iteration of the loop after an exception is caught instead of having to re-input numbs

        def video_titles(link):
            t = YouTube(link).title
            return t      

        titles_unreadable = []
        # MULTITHREADING STARTS
        with ThreadPoolExecutor() as executor:
            for url in video_links: # reference line for KeyError(Invalid URL) exception handling
                titles_unreadable.append(executor.submit(video_titles, url)) # video_titles is the function, url is the *arg/positional arguement(essentially what to feed into the function), url feeds into the link in video_titles(link)

        url_list = [] # for the program to use the urls of the videos
        titles_readable = [] # for the user to see the videos in playlist
        for task in titles_unreadable:
            titles_readable.append(task.result()) # you use the .result(), bc it only appends to the list once the video has been recieved(in multithreading, every thread takes turns, so you can't call for a video that is only partially sent)
        # MULTITHREADING ENDS

        for link in video_links:    
            url_list.append(link)
        n = int(Playlist(playlist_link).length) + 1
        r = list(range(1,n))
        new_titles = ['{} - {} - {}'.format(*t) for t in zip(r, titles_readable, video_links)]
        # *t is basically like pasting what t is in for *t, so in this case: format(zip(r, titles, video_link)), kinda
        # zip combines elements from different lists into a single element in a new list, all in order 
        for x in new_titles:
            print(x)
        print('\nlist compiled\n')

        loop_2 = True
        while loop_2 == True:
            try:

                numbs = input('List the video numbers you would like to download in this format - Ex: all or 2,4,7 or 2-4 or 2\n>>>')
                if numbs == 'all': # if user uses 1st option
                    for stuff in url_list:
                        downloading_process(stuff)
                    loop_2 = False
                elif __name__ == '__main__':
                    key_word_1 = ',' # if user uses 2nd option
                    key_word_2 = '-' # if user uses 3rd option

                    if key_word_1 in numbs:
                        numbs_list = numbs.split(',') # split converts the string between the comma into seperate strings in a list
                        for index in range(0,len(numbs_list)): # use range and not numbs_list, bc the index has to be int, not str, in order to convert the str in numbs_list into int
                            numbs_list[index] = int(numbs_list[index]) # turns all number strings in numbs_list into int/ Ex of numbs_list[index]: when the index is at int 0 it is associated with str '1', so str '1' is converted to int 1
                            numbs_list[index] -= 1  # substracts 1 from each interger in numbs_list
                        compiled_url_list = []
                        for things in numbs_list:
                            compiled_url_list.append(url_list[things])
                        for items in compiled_url_list:
                            downloading_process(items)

                    if key_word_2 in numbs:
                        numbs_list = numbs.split('-')
                        int_numbs_list = [] # used as range for indexing
                        for str in numbs_list:
                            int_numbs_list.append(int(str))
                        new_numbs_list = [] # used as index
                        for index in range(int_numbs_list[0], int_numbs_list[1] + 1):
                            index -= 1
                            new_numbs_list.append(index)
                        compiled_url_list = []
                        for things in new_numbs_list:
                            compiled_url_list.append(url_list[things])
                        for items in compiled_url_list:
                            downloading_process(items)

                    else: # if user uses 4th option
                        number = int(numbs) # reference line for Value Error exception handling
                        number -= 1
                        downloading_process(url_list[number])

                    loop_2 = False

            except ValueError: # if the user doesn't enter anything
                exc_type, exc_obj, exc_tb = sys.exc_info()
                if exc_tb.tb_lineno == 108: # this if used when there is ',', as the program refers to the 4th option after downloading the final video for some reason, which needs to be overidden
                    loop_2 = False
                else:
                    print('\nInvalid selection try again\n')
            except IndexError: # if the user enters a number that doesn't exist
                print('\nInvalid selection try again\n')
            # these exceptions don't go in the def bc, if in def, they will only be able to catch exceptions once def is run and we don't want to continue with the next iteration of the loop if these exceptions are caught
            
    except KeyError: # for urls that don't exist
        exc_type, exc_obj, exc_tb = sys.exc_info()
        if exc_tb.tb_lineno == 48: # inaccesible urls
            print('Not a valid URL\n')
            continue
        
    ending = input('\nType 1 if you have more videos to download\nType 2 if you want to close the application\n>>>')
    if ending == '2':
        break
